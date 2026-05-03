## 目标
定期获得公网ip变换信息，如果公网IP发生变换，使用邮件通知

计划
- 多种获得公网IP信息的方法
- 多样的通知方法
- 可配置

## 技术
- uv 进行项目管理
- 公网IP获取
    - 公网 IP 查询 API
- 轮询检查公网IP变换
- 通知系统
    - 邮件通知
- 配置文件
    - 轮询间隔
    - 邮箱信息

### 公网 IP 查询 API
因为不能保证API会不会挂，解析格式会不会变
所以希望社区可以反馈API变换情况，提交PR尝试修复

脚本使用百度查询API
#### 百度查询API
国内可访问, 返回json格式

```bash
curl -s https://qifu-api.baidubce.com/ip/local/geo/v1/district
```
## 源码
```python
import requests

import time

  

import smtplib # 导入smtplib库用于发送电子邮件

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.utils import formataddr, formatdate

  

# 默认配置

POLL_INTERVAL = 60  # 轮询间隔（秒）

EMAIL_USER = "your_email@example.com"

EMAIL_PASS = "your_password"

EMAIL_TO = "recipient@example.com"

  

def get_public_ip():

    """获取公网IP"""

    try:

        response = requests.get("https://qifu-api.baidubce.com/ip/local/geo/v1/district")

        response.raise_for_status()

        data = response.json()

        # 解析返回的JSON数据，提取IP字段    

        return data.get("ip", "")

  

    except Exception as e:

        print(f"获取公网IP失败: {e}")

        return None

  

def send_notification_by_qq_email(ip, sender_email, password, target_email):

    """

    发送IP变更通知邮件

    参数:

        ip (str): 新的WAN IP地址

        sender_email (str): 发件人邮箱

        password (str): 邮箱授权码/密码

        target_email (str): 收件人邮箱

    返回:

        bool: 邮件是否成功发送

    """

    max_retries = 3

    retry_delay = 5  # 秒

    for attempt in range(max_retries):

        try:

            # 构造邮件内容

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            content = f"""\

新的WAN IP地址检测通知

  

检测时间: {timestamp}

新的IP地址: {ip}

  

此邮件由IP监控系统自动发送，请勿直接回复。

"""

            msg = MIMEMultipart()

            msg["Subject"] = f"IP变更通知 - {timestamp}"

            msg["From"] = formataddr(("IP监控系统", sender_email))

            msg["To"] = formataddr(("管理员", target_email))

            msg["Date"] = formatdate(localtime=True)

            # 添加纯文本和HTML版本

            text_part = MIMEText(content, "plain", "utf-8")

            html_part = MIMEText(

                f"<html><body><h2>IP变更通知</h2>"

                f"<p>检测时间: <strong>{timestamp}</strong></p>"

                f"<p>新的IP地址: <code>{ip}</code></p>"

                f"<hr><small>自动发送，请勿回复</small></body></html>",

                "html", "utf-8"

            )

            msg.attach(text_part)

            msg.attach(html_part)

            # 发送邮件

            with smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10) as server:

                #server.set_debuglevel(1)  # 调试模式下可看到SMTP交互详情

                server.login(sender_email, password)

                server.sendmail(sender_email, [target_email], msg.as_string())

            print(f"✅ 邮件发送成功 (尝试 {attempt + 1}/{max_retries})")

            return True

        except smtplib.SMTPResponseException as e:

            # 特殊处理QQ邮箱可能返回的异常响应

            if e.smtp_code == -1 and e.smtp_error == b'\x00\x00\x00':

                print(f"⚠️ SMTP服务器返回非标准响应，但邮件可能已发送成功")

                return True

            if attempt == max_retries - 1:

                print(f"❌ 邮件发送最终失败 (SMTP错误 {e.smtp_code}: {e.smtp_error})")

                return False

            print(f"⚠️ SMTP临时错误 (尝试 {attempt + 1}/{max_retries}): {e}")

            time.sleep(retry_delay)

        except Exception as e:

            if attempt == max_retries - 1:

                print(f"❌ 邮件发送最终失败: {str(e)}")

                return False

            print(f"⚠️ 发送失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")

            time.sleep(retry_delay)

    return False

  

def main():

    """主函数"""

    last_ip = "0.0.0.0"

    while True:

        print(f"开始获取公网IP")

        current_ip = get_public_ip()

        if current_ip:

            print(f"获取公网IP成功：{current_ip}")

            if current_ip!=last_ip:

                print(f"公网ip发生变化！")

                if last_ip is not None:

                    print(f"准备发送邮件通知")

                    send_notification_by_qq_email(current_ip,EMAIL_USER,EMAIL_PASS,EMAIL_TO)

                    pass

                last_ip = current_ip

            else:

                print(f"公网IP未发送变化")

        else:

            print(f"获取公网IP失败，获取的公网IP为空")

  
  

        print(f"等待下一次获取，间隔{POLL_INTERVAL}秒")

        time.sleep(POLL_INTERVAL)

  

if __name__ == "__main__":

    main()
```