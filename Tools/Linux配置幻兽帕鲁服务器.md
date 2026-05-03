## 简单的步骤
- [x] 内网穿透  
- [x] Linux运行帕鲁服务端 
    - 下载steam
    - 安装帕鲁服务端
    - 运行服务器
    - 配置穿透
- [x] 实际测试  

### 内网穿透
使用frp进行内网穿透，具体步骤参考[frp]()
设置配置文件
```json
[[proxies]]
name = "palworld"
type = "udp"
localIP = "127.0.0.1"
localPort = 8211
remotePort = 8211
```
注意为**udp**

云服务器**记得开放防火墙**

### Linux运行帕鲁服务端
使用steamcmd来下载服务端  
具体步骤参考[steamcmd](https://developer.valvesoftware.com/wiki/Zh/SteamCMD#%E6%89%8B%E5%8A%A8%E5%AE%89%E8%A3%85)
[幻兽帕鲁社区服务器搭建架设开服教程（LINUX）](https://zhuanlan.zhihu.com/p/680966903)

### 实际测试
先内网测试

再公网测试

