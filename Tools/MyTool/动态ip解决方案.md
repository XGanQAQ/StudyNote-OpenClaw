## 参考教程
[拥有一条公网IP有多香？家庭申请公网IP方法及配置教程 - 知乎](https://zhuanlan.zhihu.com/p/665374743)
## 解决方案
- 静态ip（放弃）
    - 申请一个静态ip
    - 价格较贵，只有公司可以申请
- 路由器DDNS动态域名解析（放弃）
    - 通过域名解析到公网ip
	    - 通过域名访问设备
	    - 域名解析服务付费
    - 官方光猫不支持DDNS
	    - 需要桥接光猫，额外的路由器
- 使用脚本（采用）
    - 通过脚本获取公网ip
    - 通过脚本发送到邮箱
    - 通过脚本配置DDNS
    - 免费
    - 个人使用没问题，但是没办法给别人使用

## 我的方案
在服务器上部署一个脚本，每隔一段时间登陆本地网关控制网站爬取公网ip信息，如果发生变化，就通过邮箱发送给我。
我设想的进一步是发生变化就自动配置DDNS，但是由于我暂未使用域名，所以暂时没完成这个功能。
我的网关是TP-Link电信的，可能对于不同平台的网关设备的管理界面，需要特定的爬取方法，请更具自己的设备做个性化调整。

## 动态ip解决脚本
一个从网关管理界面拉取信息的工具
- 爬取ip信息
    - 每隔1小时爬取一次
- 发送到对应设备
    - 使用邮箱发送通知
- DDNS配置（未完成）
    - 使用阿里云的DDNS服务
    - 通过脚本配置DDNS
    - 通过脚本修改域名解析

## 遇到的问题
我在windows上很快完成了这个脚本，但是在linux上却遇到了很多问题
首先是selenium的chrome驱动问题，它无法自动下载
于是我手动下载了对应的驱动，写明了路径，解决此问题

systemctl服务配置问题，原先ai说需要使用虚拟屏幕环境，但是实际不需要。只需要把selenium的配置添加--headless参数即可


## 源码
```python
import sys # 导入sys模块以获取命令行参数

import requests # 导入requests库用于发送HTTP请求
from bs4 import BeautifulSoup

from selenium import webdriver # 导入selenium库用于自动化浏览器操作
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time

import traceback  # 导入traceback模块以获取完整的错误信息

import smtplib # 导入smtplib库用于发送电子邮件
from email.mime.text import MIMEText
from email.utils import formataddr


ROUTER_IP = "your_router_ip"  # 替换为路由器IP地址
USERNAME = "your_username"  # 替换为路由器登录用户名
PASSWORD = "your_password"  # 替换为路由器登录密码
WANIP = "0.0.0.0"  # 初始WAN IP地址

CHECK_GAP = 60 * 60  # 检查间隔时间（秒），1小时

SENDER_EMAIL = "your_email@example.com"  # 替换为发送通知的邮箱
QQ_EMAIL_PASSWORD = "your_email_password"  # 替换为邮箱的授权码或密码
TARGET_EMAIL = "target_email@example.com"  # 替换为目标邮箱

ChromeDriverPath = "/path/to/chromedriver"  # 替换为ChromeDriver的路径

def selenium_login():
    # 配置Chrome选项（可选）
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式必须
    chrome_options.add_argument("--no-sandbox")  # Linux 必加
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = webdriver.ChromeService(executable_path=ChromeDriverPath)  # 修改为你的路径
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(f"http://{ROUTER_IP}/cgi-bin/luci")
        
        # 关键修复：等待元素可交互（最多等10秒）
        wait = WebDriverWait(driver, 3)
        
        # 方法1：直接移除disabled属性（更可靠）
        driver.execute_script("""
            document.getElementById("login_username").removeAttribute("disabled");
            document.getElementById("login_password").removeAttribute("disabled");
        """)
        
        # 方法2：传统等待方式
        username_field = wait.until(
            EC.element_to_be_clickable((By.ID, "login_username"))
        )
        password_field = wait.until(
            EC.element_to_be_clickable((By.ID, "login_password"))
        )
        
        # 输入凭据
        username_field.clear()
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)

        
        # 提交登录
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_button.click()
        
        # 验证登录
        time.sleep(3)
        if "/cgi-bin/luci/" in driver.current_url:
            print("✅ 登录成功")
            return driver;
        else:
            print("❌ 登录失败，当前URL:", driver.current_url)
            driver.save_screenshot("login_fail.png")

    except Exception as e:
        print("\n❌ 完整错误信息:")
        print(traceback.format_exc())  # 关键修改：打印完整错误
def get_ip_from_html(driver):
    try:
        driver.get(f"http://{ROUTER_IP}/cgi-bin/luci/admin/settings/info")
        time.sleep(1.5)  # 等待页面加载完成

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # 解析IP地址
        ip_element = soup.find("span", id="WANIP")
        if ip_element:
            wan_ip = ip_element.text.strip()
            return wan_ip
        else:
            print("❌ 无法找到WAN IP元素")
            return None

    except Exception as e:
        print("\n❌ 完整错误信息:")
        raise
def send_notification_by_email(ip, sender_email, password, target_email):
    try:
        content = f"新的WAN IP地址是 {ip}"
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = "WAN IP地址变化通知"
        msg["From"] = formataddr(("IP监控系统", sender_email))
        msg["To"] = formataddr(("管理员", target_email)) 

        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, [target_email], msg.as_string())

        print("✅ 邮件发送成功（即使可能报错，但邮件已送达）")

    except smtplib.SMTPResponseException as e:
        # 忽略SMTP关闭时的异常（如果邮件已发送成功）
        print(f"⚠️ SMTP服务器返回异常，但邮件可能已发送: {e}")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        raise
def check_ip():
    """
    检查IP地址是否变化
    变化返回True，否则返回False

    """
    driver = selenium_login()
    global WANIP
    if driver:
        newWANIP = get_ip_from_html(driver)
        if newWANIP == WANIP:
            print("✅ WAN IP 没有变化",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            driver.quit()
            return False;
        else:
            print("✅ WAN IP 发生变化:", newWANIP,"当前查询时间为：" ,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            WANIP = newWANIP
            driver.quit()
            return True;
    else:
        print("❌ 无法获取新的WAN IP, 请检查登录是否成功")
        driver.quit()
        return False;   

if __name__ == "__main__":
    print("Start")
    while True:
        if(check_ip()):
            print("ready to send email")
            send_notification_by_email(WANIP, SENDER_EMAIL, QQ_EMAIL_PASSWORD, TARGET_EMAIL)
        
        time.sleep(CHECK_GAP)  # 等待指定的检查间隔时间
    
```

常用命令
```bash
sudo journalctl -u 服务名.service -n 50  # 查看最近 50 行
```
