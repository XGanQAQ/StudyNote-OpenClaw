# Unity 世界的三种对象（完整世界观版）

> Unity **不是一个纯 C# 程序**  
> 它是：**C#（托管世界） + C++（引擎世界）** 的混合系统
> 
> 所以——  
> **Unity 的“对象”，天然就分世界**

---

## 总览：三种对象一眼速览

|类型|所属世界|代表|谁创建|谁销毁|
|---|---|---|---|---|
|① 纯 C# 对象|CLR / 托管|`new` 出来的类|你|GC|
|② Unity 引擎对象|C++ 引擎|GameObject / SO|Unity|Unity|
|③ Unity 资源对象|引擎 + 资产系统|`.asset / prefab`|Unity|Unity|

你真正困惑的，**全在 ② 和 ③ 的交界处**。

我们一个一个来。

---

# 一、第一种：纯 C# 对象（你最熟的世界）

## 1️⃣ 它是什么？

**完全遵守 C# / .NET 规则的对象**

```csharp
class WeaponRuntime
{
    public int level;
}

var w = new WeaponRuntime();
```

---

## 2️⃣ 它的特征（非常干净）

- 用 `new` 创建
    
- 在 **托管堆（Managed Heap）**
    
- 生命周期由 **GC 决定**
    
- Unity **完全不感知**
    
- 不会显示在 Inspector
    
- 不会被序列化成资源
    

📌 **Unity 看不到它 = Unity 不会救你**

---

## 3️⃣ 它适合干什么？

✅ **一切运行时状态**

- 玩家状态
    
- 战斗中数据
    
- Buff / CD / 临时数值
    
- 网络同步结构
    
- 存档数据结构
    

📌 **一句话**

> 凡是“会变的”，几乎都该是纯 C# 对象

---

## 4️⃣ 它的世界观定位

> 这是**程序员的世界**  
> 干净、可控、理性、符合常识

---

# 二、第二种：Unity 引擎对象（UnityEngine.Object）

这一步是**断层点**，很多 Unity 开发者一辈子都没想明白。

---

## 1️⃣ 它是什么？

**存在于 Unity 引擎（C++）中的对象**  
C# 里只是一个“壳 / 句柄”。

```csharp
GameObject
Component
MonoBehaviour
ScriptableObject
Texture
AudioClip
```

👉 **它们全部继承 `UnityEngine.Object`**

---

## 2️⃣ 最关键的一句话（⚠️）

> **UnityEngine.Object 不是 C# 对象  
> 它只是“被 C# 引用的引擎对象”**

真实结构是：

```
C++ 引擎对象
     ↑
C# Object 句柄（UnityEngine.Object）
```

---

## 3️⃣ 它是怎么创建的？

❌ **不能用 `new`**

```csharp
new GameObject(); // ❌ 错误理解
```

✅ 正确方式：

```csharp
new GameObject("Player"); // 表面上 new，实际上走 Unity 内部
Instantiate(prefab);
CreateInstance<ScriptableObject>();
```

📌 所有创建最终都走：

> **Unity C++ 引擎分配内存**

---

## 4️⃣ 生命周期是谁管？

**不是 GC，而是 Unity**

```csharp
Destroy(gameObject);
```

- 你不 Destroy
    
- GC 也不会回收
    
- 内存会一直挂着
    

---

## 5️⃣ 为什么 `obj == null` 会很诡异？

因为 Unity 做了 **“伪 null”**

```csharp
if (obj == null)
```

其实在问：

> “这个 C++ 对象还活着吗？”

即使 C# 引用还在。

📌 **这不是语言特性，是 Unity 魔法**

---

## 6️⃣ 适合干什么？

✅ **和场景 / 表现 / 引擎强相关的东西**

- 场景物体
    
- 组件
    
- 渲染资源
    
- 配置资产（SO）
    

📌 **一句话**

> 凡是“看得见 / 能拖拽 / 能序列化”的，基本都在这里

---

# 三、第三种：Unity 资源对象（Asset Instance）

🔥 **这是你真正困惑的那一类**

---

## 1️⃣ 它是什么？

> **被资产系统管理的 Unity 引擎对象**

- `.asset`
    
- `.prefab`
    
- `.mat`
    
- `.controller`
    

它们是：

> **“持久化的 UnityEngine.Object 实例”**

---

## 2️⃣ 关键认知（非常重要）

> **资源文件 ≠ 类定义  
> 资源文件 = 一个“已经存在的实例”**

---

## 3️⃣ 举个直观例子（ScriptableObject）

```csharp
WeaponConfigSO.asset
```

它代表的不是：

```text
WeaponConfigSO 这个类
```

而是：

```text
WeaponConfigSO 的一个“具体实例”
```

就像数据库里的一行记录。

---

## 4️⃣ 它是什么时候被创建的？

### 编辑器阶段

```text
右键 Create → SO
```

Unity 会：

1. 在引擎里创建对象
    
2. 分配内存
    
3. 序列化成 `.asset`
    

📌 **那一刻它就已经是“实例”了**

---

## 5️⃣ 运行时发生了什么？

当你：

- 引用它
    
- 加载它
    
- Inspector 显示它
    

Unity 会：

```
.asset 文件
   ↓ 反序列化
引擎内存对象
   ↓
C# 句柄
```

你只是“拿到引用”，不是 new。

---

## 6️⃣ 为什么它看起来像“全局单例”？

因为：

> **一个 Asset 文件 = 一个实例**

```csharp
a.weaponConfig
b.weaponConfig
c.weaponConfig
```

全部指向同一个对象。

📌 这就是：

- SO 被当配置
    
- Prefab 被当模板
    

的原因。

---

## 7️⃣ 为什么修改 SO 会“污染所有人”？

因为你改的是：

> **那个唯一实例**

```csharp
weaponConfig.damage += 10; // 所有人一起变
```

---

# 四、三种对象的“边界法则”（请背）

## 1️⃣ 谁能 `new`？

|类型|能不能 new|
|---|---|
|纯 C#|✅|
|Unity 引擎对象|❌|
|资源对象|❌|

---

## 2️⃣ 谁能存档？

|类型|能不能直接存|
|---|---|
|纯 C#|✅|
|Unity 引擎对象|❌|
|资源对象|❌|

---

## 3️⃣ 谁适合当配置？

|类型|适合度|
|---|---|
|纯 C#|❌|
|Unity 引擎对象|⚠️|
|资源对象（SO）|✅|

---

# 五、一句“程序员该有的世界观总结”

> **Unity 是一个“双世界引擎”  
> C# 负责“逻辑和状态”  
> Unity 引擎负责“存在和表现”**

ScriptableObject、Prefab 之所以“反直觉”，  
是因为它们**根本不活在 C# 的世界里**。