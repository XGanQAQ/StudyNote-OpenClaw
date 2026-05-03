## 1.下载Linux
执行 mkdir ~/clash; cd ~/clash 在用户目录下创建 clash 文件夹。

下载适合的 Clash 二进制文件，解压，并将解压产物重命名为 clash

https://github.com/DustinWin/clash_singbox-tools/releases/tag/Clash-Premium

注：一般个人的64位电脑下载 clashpremium-release-linux-amd64.tar.gz 即可。

## 2.下载配置文件
在终端 cd 到 Clash 二进制文件所在的目录，执行 wget -O config.yaml "https://c8wql.no-mad-world.club/link/8YcsosUEOECa6H98?clash=3" 下载 Clash 配置文件

## 3.启动 Clash
找到可执行文件 clash，执行 ./clash -d .
注意可执行文件的名字可能不叫clash，找对对应的打开即可，我的下载的clash名字为CrshCore  
即可启动 Clash，同时启动 HTTP 代理和 Socks5 代理。

如提示权限不足，请执行 chmod +x clash

## 4.访问Web面板
在确保Clash核心已经启动的情况下，打开浏览器，访问 https://clash.razord.top/

## 5.配置主机代理设置
以 Ubuntu 19.04 为例，打开系统设置，选择网络，点击网络代理右边的 ⚙ 按钮，选择手动，填写 HTTP 和 HTTPS 代理为 127.0.0.1:7890，填写 Socks 主机为 127.0.0.1:7891，即可启用系统代理。