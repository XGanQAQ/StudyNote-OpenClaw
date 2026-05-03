在 Unity 里，**ScriptableObject 的 `OnEnable` / `OnDisable` 生命周期和 MonoBehaviour 很不一样**，这也是很多人容易踩坑的地方。我们分**结论 → 触发时机 → 常见坑 → 实战建议**来讲。

---

## 一句话结论（先记住这个）

> **ScriptableObject 的 `OnEnable` / `OnDisable` 是“资源加载 / 卸载级别”的事件，而不是“游戏运行级别”的事件。**

它们**不代表对象被使用 / 停用**，而是：

- **被加载到内存时 → `OnEnable`**
    
- **从内存中卸载时 → `OnDisable`**
    

---

## 一、`OnEnable` 什么时候会触发？

### 1️⃣ ScriptableObject 被加载到内存时（最常见）

包括但不限于：

- **Unity 编辑器启动 / 重新加载脚本（Domain Reload）**
    
- 某个 `ScriptableObject` **第一次被引用**
    
    - 被 Inspector 显示
        
    - 被某个脚本字段引用
        
    - 被 `Resources.Load` / Addressables 加载
        
- **进入 Play Mode**
    
- **切换场景**（如果该 SO 被新场景引用）
    

📌 **哪怕你什么都没写代码，只要它被“看到”或“用到”，就可能触发**

---

### 2️⃣ Play Mode 期间重新加载

以下操作也会触发：

- 脚本重新编译
    
- 重新进入 Play Mode
    
- Assembly Reload（如果没关）
    

---

### 3️⃣ 示例

```csharp
[CreateAssetMenu]
public class GameConfig : ScriptableObject
{
    private void OnEnable()
    {
        Debug.Log("GameConfig OnEnable");
    }
}
```

你会发现：

- 打开 Inspector → 打印
    
- 进 Play → 打印
    
- 退 Play → 可能再打印一次
    
- 重编译 → 又打印
    

---

## 二、`OnDisable` 什么时候会触发？

### 1️⃣ ScriptableObject 从内存卸载时

典型情况：

- 退出 Play Mode
    
- 编辑器 Domain Reload
    
- 脚本重新编译
    
- 编辑器关闭
    
- Addressables / Resources 卸载该资源
    

📌 **不是你“不用它了”，而是 Unity 决定把它从内存移走**

---

### 2️⃣ 注意：并不保证一定调用

这是一个**非常重要的坑点**：

> ❗ **ScriptableObject 的 `OnDisable` 并不保证每次都会被调用**

例如：

- Unity 崩溃
    
- 强制关闭编辑器
    
- 某些 GC / 内部卸载流程
    

👉 **不要把关键逻辑（保存数据、网络断连）放在 `OnDisable` 里**

---

## 三、和 MonoBehaviour 的核心区别（重点）

|对比点|MonoBehaviour|ScriptableObject|
|---|---|---|
|含义|组件启用/禁用|资源加载/卸载|
|`OnEnable`|GameObject 激活|SO 进内存|
|`OnDisable`|GameObject 失活|SO 出内存|
|是否可控|高（SetActive）|低（Unity 管理）|
|生命周期稳定性|稳定|**不稳定**|

👉 **ScriptableObject 没有 `Start / Update`，本质是“数据资产”**

---

## 四、几个常见误区（强烈建议避开）

### ❌ 误区 1：把 `OnEnable` 当初始化函数

```csharp
void OnEnable()
{
    hp = maxHp; // ❌ 很可能被反复重置
}
```

💥 后果：

- 切场景
    
- 重编译
    
- 打开 Inspector  
    👉 全部都会把数据重置
    

---

### ❌ 误区 2：用 `OnDisable` 做存档 / 清理

```csharp
void OnDisable()
{
    SaveGame(); // ❌ 不可靠
}
```

👉 可能**永远不调用**

---

### ❌ 误区 3：以为 ScriptableObject 是“运行时唯一实例”

实际上：

- Inspector 中看到的是 **Asset**
    
- 运行时可能：
    
    - 直接用 Asset（危险）
        
    - 或 `Instantiate` 出 Runtime 副本（推荐）
        

---

## 五、推荐的正确使用方式（实战经验）

### ✅ 1️⃣ `OnEnable` 只做「轻量级、幂等」初始化

适合做：

- 缓存字段
    
- 事件注册（可重复）
    
- 状态校验
    

```csharp
void OnEnable()
{
    if (list == null)
        list = new List<int>();
}
```

---

### ✅ 2️⃣ 明确区分「资产数据」和「运行时数据」

**推荐模式：**

```csharp
[CreateAssetMenu]
public class CardData : ScriptableObject
{
    public int baseDamage;

    public RuntimeCard CreateRuntime()
    {
        return new RuntimeCard(this);
    }
}
```

```csharp
public class RuntimeCard
{
    public int damage;

    public RuntimeCard(CardData data)
    {
        damage = data.baseDamage;
    }
}
```

👉 **不要在 ScriptableObject 里存“会变化的运行时状态”**

---

### ✅ 3️⃣ 如果你真的需要运行时生命周期

请用：

- `GameManager`
    
- `MonoBehaviour`
    
- 明确的 `Init()` / `Dispose()` 方法
    

```csharp
public void Init()
{
    // 明确、可控
}
```

---

## 六、结合你的背景给一句建议

你现在**大量在做游戏系统设计（卡牌 / 任务 / 数据驱动）**，非常容易用 ScriptableObject 当“逻辑对象”。

👉 **记住这条铁律：**

> **ScriptableObject = 配置 & 原型  
> 运行时状态 = 普通类 / MonoBehaviour**

只要守住这条，你几乎不会踩生命周期坑。