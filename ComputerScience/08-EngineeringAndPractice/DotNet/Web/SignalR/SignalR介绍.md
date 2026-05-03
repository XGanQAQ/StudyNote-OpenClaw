SignalR 是 .NET 平台上一个非常强大的实时通信库，适用于 Web 应用、移动应用和桌面应用等多种场景。它可以让服务器主动向客户端推送消息，从而实现实时更新，比如聊天室、通知、实时图表等。

---

## 🌐 什么是 SignalR？

**SignalR** 是 Microsoft 提供的一个 **实时通信库**，它基于 ASP.NET 或 ASP.NET Core，能实现：

- **服务器推送**（Server push）
    
- **双向通信**（客户端与服务器之间可互相发送消息）
    
- **自动选择传输方式**（WebSockets、Server-Sent Events、长轮询）
    
- **连接管理**（跟踪每个连接的客户端，支持广播、单播）
    

---

## ✅ SignalR 的适用场景

|场景|说明|
|---|---|
|实时聊天系统|聊天室、客服系统|
|实时游戏|多人在线游戏状态同步|
|实时通知|提醒、告警、系统消息|
|协同编辑|在线文档协作|
|实时数据展示|实时图表、股价、传感器数据|

---

## 🛠️ SignalR 架构核心组件

1. **Hub（中心）**
    
    - 服务器端的主要通信入口，客户端通过它调用服务器方法，反之亦然。
        
2. **ConnectionId**
    
    - 每个客户端连接会有唯一的 ID，用于定向发送消息。
        
3. **Group**
    
    - 可以将多个连接加入一个组，用于组播。
        
4. **User**
    
    - 支持基于用户标识发送消息（需要身份认证支持）。
        

---

## 🚀 开发体验流程（基于 ASP.NET Core SignalR）

### 1. 安装依赖

```bash
dotnet add package Microsoft.AspNetCore.SignalR
```

### 2. 创建 Hub 类（服务端）

```csharp
public class ChatHub : Hub
{
    public async Task SendMessage(string user, string message)
    {
        await Clients.All.SendAsync("ReceiveMessage", user, message);
    }
}
```

### 3. 注册 SignalR（在 `Startup.cs` 或 `Program.cs`）

```csharp
app.MapHub<ChatHub>("/chathub");
```

### 4. 客户端（JavaScript）

```html
<script src="https://cdn.jsdelivr.net/npm/@microsoft/signalr@latest/dist/browser/signalr.js"></script>
<script>
    const connection = new signalR.HubConnectionBuilder()
        .withUrl("/chathub")
        .build();

    connection.on("ReceiveMessage", (user, message) => {
        console.log(`${user}: ${message}`);
    });

    connection.start().then(() => {
        connection.invoke("SendMessage", "小明", "你好 SignalR！");
    });
</script>
```

---

## ⚙️ 传输协议支持

SignalR 会根据环境自动选择传输方式（也可以手动配置）：

- **WebSockets（首选）**
    
- **Server-Sent Events（SSE）**
    
- **Long Polling**
    

---

## 🔐 支持身份认证和授权

SignalR 支持基于 ASP.NET Core 的身份认证机制，你可以通过 `Context.User` 获取用户信息，并可基于此实现：

- 对消息的授权控制
    
- 对用户发送定向消息
    

---

## 📡 扩展支持

- **ASP.NET Core SignalR** 支持 **Azure SignalR 服务**，可以轻松扩展到千万级连接。
    
- 支持多语言客户端，如 JavaScript、.NET、Java、Python（通过第三方库）。
    

---

## 🧪 示例项目推荐

你可以尝试这个基础聊天室项目：

- 服务端：ASP.NET Core Web 应用
    
- 客户端：HTML + JavaScript
    
- 功能：发送/接收消息、用户连接通知
    