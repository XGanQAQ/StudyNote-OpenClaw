为了越过墙的问题，采用本地发送文件到服务器的方式，配置ftp。

## 本地下载ftp，并发送到服务器
使用scp命令，将ftp文件发送到服务器
```shell
scp -r filename username@hostname:/path/to/directory
```

## 配置ftp配置文件
配置服务器端
```bash
# frps.toml
# 基本配置
bindPort = 7000           # frps 监听的端口，用于接收 frpc 的连接
# 认证配置
[auth]
method = "token"          # 认证方法，这里使用 token
token = "kT9j$Xp1&7sL"  # 用于验证 frpc 的 token，请使用安全的随机字符串

# Web 管理界面配置（如果不需要 Web 管理界面，可以删除这部分）
[webServer]
addr = "0.0.0.0"          # Web 界面监听的地址，0.0.0.0 表示所有地址
port = 7500               # Web 界面的端口
user = "xgan"            # Web 界面的登录用户名
password = "1246652674Aa@"  # Web 界面的登录密码

# 日志配置
[log]
to = "console"            # 日志输出位置，console 表示输出到控制台
level = "info"            # 日志级别：debug, info, warn, error
```
配置客户端
```bash
serverAddr = "117.72.87.106"
serverPort = 7000

auth.method = "token"
auth.token = "kT9j$Xp1&7sL"

[[proxies]]
name = "ssh"
type = "tcp"
localIP = "127.0.0.1"
localPort = 22
remotePort = 2222

[[proxies]]
name = "blink"
type = "tcp"
localIP = "127.0.0.1"
localPort = 1111
remotePort = 6111
```

## 服务器使用守护进程启动frp服务器
```bash
./frps -c frps.toml 
```

## 客户端连接服务器
```bash
./frpc -c frpc.toml
```

## 云服务器启动开放安全组（防火墙）