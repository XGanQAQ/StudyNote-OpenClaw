# ✅ **Mirror 网络同步脚本常用调用提纲（结构化）**

下面以 _NetworkBehaviour 负责同步，MonoBehaviour 负责本地逻辑_ 的思路，给你梳理最常用的 Mirror 调用结构与用途。

---

# 1. **基础字段同步（[SyncVar]）**

### 📌 场景：

血量、状态、小量数据同步

### 使用方式

```csharp
[SyncVar(hook = nameof(OnHpChanged))]
private int hp;

void OnHpChanged(int oldValue, int newValue)
{
    // 客户端 UI 更新
}
```

### 注意

- **只能在服务器上修改**（Server-only）
    
- Hook 在所有客户端自动触发（不含服务器旧值 → 新值序列）
    

---

# 2. **远程调用（Command / ClientRpc / TargetRpc）**

## 2.1 **Command（客户端 → 服务器）**

用于：玩家输入、发起攻击、请求交互等

```csharp
[Command]
void CmdFire(Vector3 dir)
{
    // 服务端执行：创建子弹、验证逻辑、广播
}
```

- 只能客户端调用
    
- 在服务器执行
    
- 只能调用**自己对象**上的 Command（需要authority）
    

---

## 2.2 **ClientRpc（服务器 → 所有客户端）**

用于：广播事件、特效、生成物体通知等

```csharp
[ClientRpc]
void RpcPlayShootFX()
{
    // 在所有客户端播放特效
}
```

- 服务端调用
    
- 所有客户端执行
    
- 不需要NetId范围限制
    

---

## 2.3 **TargetRpc（服务器 → 特定客户端）**

用于：UI提示、玩家私有信息、同步背包更新等

```csharp
[TargetRpc]
void TargetShowMessage(NetworkConnectionToClient conn, string msg)
{
    UI.Show(msg);
}
```

---

# 3. **网络物体生成（Spawn / Destroy）**

## 3.1 服务端生成并同步给所有客户端

```csharp
GameObject bullet = Instantiate(bulletPrefab);
NetworkServer.Spawn(bullet);
```

## 3.2 销毁网络对象

```csharp
NetworkServer.Destroy(obj);
```

⚠️客户端不可直接 Instantiate → Spawn

---

# 4. **网络权限（Authority）相关**

## 4.1 典型使用：移动、输入由本地玩家控制

```csharp
public override void OnStartAuthority()
{
    enabled = true; // 只有自己能启用控制逻辑
}
```

## 4.2 服务器授予权限

```csharp
NetworkIdentity.AssignClientAuthority(conn);
```

---

# 5. **NetworkTransform / 自定义位置同步**

## 5.1 使用官方组件

- NetworkTransform
    
- NetworkRigidbody
    

## 5.2 自定义同步（推荐你当前项目使用）

```csharp
[SyncVar] Vector3 syncPos;

[Command]
void CmdUpdatePosition(Vector3 pos)
{
    syncPos = pos;
}

void Update()
{
    if (isLocalPlayer)
    {
        CmdUpdatePosition(transform.position);
    }
    else
    {
        transform.position = Vector3.Lerp(transform.position, syncPos, 0.2f);
    }
}
```

---

# 6. **网络事件（OnStartServer / OnStartClient）**

常用生命周期函数：

```csharp
public override void OnStartServer() { }
public override void OnStartClient() { }
public override void OnStopServer() { }
public override void OnStopClient() { }

public override void OnStartAuthority() { }
public override void OnStopAuthority() { }
```

常用于：

- 初始化数据
    
- 注册管理器
    
- 权限相关设置
    

---

# 7. **同步 Collections（SyncList/SyncDictionary）**

## 7.1 SyncList 使用方式

```csharp
public class SyncListInt : SyncList<int> {}

public SyncListInt itemList = new SyncListInt();

private void Start()
{
    itemList.Callback += OnListChanged;
}
```

用于：

- 背包
    
- 玩家列表
    
- 任务清单
    

---

# 8. **网络消息（NetworkMessage）自定义消息通信**

（适合你的多人射击项目：低频 RPC 替代）

```csharp
public struct HitMessage : NetworkMessage {
    public uint targetId;
    public int damage;
}

NetworkServer.RegisterHandler<HitMessage>(OnHitReceived);

NetworkClient.Send(new HitMessage { targetId = id, damage = 10});
```

---

# 9. **多人射击常用同步架构模板（建议你用）**

### ① 客户端：输入 → 本地立即播放子弹

### ② 客户端：Command 向服务器提交命中报告

### ③ 服务器：验证 → 扣血 → Rpc 给所有客户端显示效果

### ④ 客户端：RPC 生成其他玩家的子弹

---

# 10. **完整推荐模版：NetworkBehaviour 标准脚本结构**

```csharp
using Mirror;
using UnityEngine;

public class PlayerNetworkController : NetworkBehaviour
{
    #region SyncVars
    [SyncVar(hook = nameof(OnHpChanged))]
    private int hp;
    #endregion

    #region Unity / Mirror Events
    public override void OnStartAuthority()
    {
        // Enable control
    }

    public override void OnStartClient()
    {
        // Init client stuff
    }
    #endregion

    #region Commands （客户端 → 服务器）
    [Command]
    void CmdFire(Vector3 dir)
    {
        // Validate
        // Spawn bullet
        RpcPlayFireFX();
    }
    #endregion

    #region ClientRpc （服务器 → 所有客户端）
    [ClientRpc]
    void RpcPlayFireFX()
    {
        // Show effect
    }
    #endregion

    #region Hooks
    void OnHpChanged(int oldValue, int newValue)
    {
        // Update UI
    }
    #endregion

    #region Public API
    public void LocalFire()
    {
        if (hasAuthority)
        {
            // local fire
            CmdFire(transform.forward);
        }
    }
    #endregion
}
```