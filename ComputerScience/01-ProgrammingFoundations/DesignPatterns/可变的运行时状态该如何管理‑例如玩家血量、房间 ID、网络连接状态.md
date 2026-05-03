把“可变运行时状态”从**全局可变单例**拆成**“生命周期明确、作用域受限、可随时重置”**的三种容器。  
下面给出 **Unity 4 人联机射击**场景下的**实战落地方案**（可直接拷用）。

------------------------------------------------
1. 玩家私有状态 → **PlayerContext（跟随玩家实体）**
- **存储位置**：挂在 **Player GameObject** 的脚本 `PlayerContext`。  
- **生命周期**：随玩家 Spawn / Despawn 创建销毁。  
- **内容**：HP、Ammo、Buff 列表。  
- **代码**：
```csharp
public class PlayerContext : MonoBehaviour
{
    [SyncVar] public int HP = 100;          // Mirror 网络同步
    public int Ammo  { get; private set; } = 30;

    public void TakeDamage(int dmg)
    {
        HP = Mathf.Max(0, HP - dmg);
        if (HP == 0) EventBus.Raise(new PlayerDied(netId));
    }

    public void Reset()        // 对象池回收时调用
    {
        HP = 100;
        Ammo = 30;
    }
}
```
- **获取方式**：别人通过 `player.GetComponent<PlayerContext>()` 访问，**绝不全局单例**。

------------------------------------------------
2. 房间/对局级状态 → **RoomSession（随房间创建销毁）**
- **存储位置**：**NetworkRoomManager** 或 **自定义 Session 对象**。  
- **生命周期**：当所有玩家进入房间时 new，房间关闭时 Dispose。  
- **内容**：房间 ID、当前波次、任务进度、掉落表种子。  
- **代码**：
```csharp
public class RoomSession : IDisposable
{
    public static RoomSession I { get; private set; }   // 作用域单例，非全局！

    public string RoomId { get; }
    public int WaveIndex { get; private set; }

    public static void Create(string roomId)
    {
        I?.Dispose();
        I = new RoomSession(roomId);
    }

    public void Dispose()
    {
        // 清理事件、保存战绩
        I = null;
    }
}
```
- **使用**：脚本只在 **Room 场景** 里通过 `RoomSession.I` 读取，**离开房间即销毁**。

------------------------------------------------
3. 网络连接状态 → **NetworkClientSession（连接生命周期）**
- **存储位置**：**NetworkClient** 或 **自定义 NetworkSession**。  
- **生命周期**：随客户端连接/断线创建销毁。  
- **内容**：RTT、丢包率、连接状态枚举。  
- **代码**：
```csharp
public class NetworkClientSession
{
    public static NetworkClientSession I { get; private set; }

    public bool IsConnected => Transport.activeTransport != null && Transport.activeTransport.ClientConnected();
    public float RTT { get; private set; }

    public static void Start()
    {
        I = new NetworkClientSession();
    }

    public static void Shutdown()
    {
        I?.Dispose();
        I = null;
    }
}
```

------------------------------------------------
4. 通用原则（背下来即可）

| 状态范围 | 容器 | 生命周期 | 销毁/重置方式 |
|---|---|---|---|
| 单玩家 | PlayerContext | Spawn/Despawn | `Reset()` 或 Destroy |
| 单房间 | RoomSession | 房间创建/关闭 | `Dispose()` |
| 单客户端 | NetworkClientSession | 连接/断线 | `Shutdown()` |
| 全局只读 | 单例 | 进程级 | 不销毁 |

------------------------------------------------
一句话总结  
**“可变状态 = 最小作用域容器 + 显式生命周期 + Reset/Dispose 钩子”**。  
把它放在“会一起生、一起死”的对象里，而不是任何全局单例里，就能避免脏状态、内存泄漏、测试地狱三大坑。