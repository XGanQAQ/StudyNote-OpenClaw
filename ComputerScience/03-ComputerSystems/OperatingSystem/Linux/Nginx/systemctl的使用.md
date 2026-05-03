## 背景
我在我的服务器上使用systemctl为我的frp和我的个人网站配置服务，但是在使用systemctl的时候，我发现有一些问题，所以我写了这篇文章来记录一下systemctl的使用方法。

## 如何书写systemctl的服务文件
systemctl的服务文件一般存放在`/etc/systemd/system/`目录下，文件的后缀名是`.service`。下面是一个systemctl的服务文件的例子：
```shell
[Unit]
Description=MyPersonWeb, a web that show myself
After=network.target

[Service]
ExecStart=/home/xgan/server/myPersonWeb_Linux_x64_self/publish/MyPersonWeb
WorkingDirectory=/home/xgan/server/myPersonWeb_Linux_x64_self/publish
Restart=always
User=xgan
Environment=ASPNETCORE_ENVIRONMENT=Production
Environment=DOTNET_ROOT=/usr/share/dotnet
Environment=WebRootPath=/home/xgan/server/myPersonWeb_Linux_x64_self/publish/wwwroot

[Install]
WantedBy=multi-user.target
```
想要自己添加一个服务，也就是要写一个这样的配置文件，然后放到`/etc/systemd/system/`目录下。

在使用AI生成的时候，它给命令后面使用#注释，这样会导致systemctl启动失败，所以要把这些注释去掉。

## systemctl的常用命令
用这几个命令基本可以覆盖所有场景了
```shell
systemctl start myService.service # 启动服务
systemctl stop myService.service # 停止服务
systemctl restart myService.service # 重启服务
systemctl status myService.service # 查看服务状态
systemctl enable myService.service # 开机自启动
systemctl disable myService.service # 取消开机自启动
systemctl daemon-reload # 重新加载配置文件
```

## Bug修复
### frp
frp启动失败，原本是直接单单只有启动命令，后来我添加了-c 配置文件路径，修复了bug。

### 个人网站
在配置我的个人网站的服务的时候，我发现服务器启动警告没找到wwwroot目录，于是我添加了`Environment=WebRootPath=/home/xgan/server/myPersonWeb_Linux_x64_self/publish/wwwroot`配置。修复了bug。
