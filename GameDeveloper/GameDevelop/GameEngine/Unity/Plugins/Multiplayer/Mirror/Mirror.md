
- NetworkManager
	- Transfrom 传输方式
	- 设置玩家预制体

- NetworkBehaviour 联机Mono脚本

## Remote Aciton
网络系统中有两种类型的RPC：
- 命令调用——由客户端调用并在服务器上执行；
- 客户端 RPC 调用——由服务器调用并在客户端执行。


- Commond
	- This function will now be run on the server when it is called on the client. Any parameters of [allowed data type](https://mirror-networking.gitbook.io/docs/manual/guides/data-types) will be automatically passed to the server with the command.
	- 现在，当客户端调用此函数时，它将在服务器端运行。任何[允许数据类型](https://mirror-networking.gitbook.io/docs/manual/guides/data-types)的参数都将随命令自动传递到服务器。

### ⭐ Command：

> 客户端 → 服务器  
> 执行位置：服务器的玩家对象

### ⭐ ClientRpc：

> 服务器 → 所有客户端  
> 执行位置：客户端的该对象镜像（包括本地玩家）

## 小记
host  =  server + client
server
client

## 参考教程
[(25 封私信 / 40 条消息) Unity 多人联机库Mirror教程 - 知乎](https://zhuanlan.zhihu.com/p/1902124152866969041)

