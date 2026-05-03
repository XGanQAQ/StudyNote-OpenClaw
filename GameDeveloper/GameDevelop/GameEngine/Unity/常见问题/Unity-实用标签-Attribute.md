在 Unity 里，“**实用的标签**”一般指的是 **C# Attribute（特性）**，它们主要用于：

- ✨ 改善 Inspector 可用性
    
- 🧠 约束数据合法性
    
- 🛠 减少样板代码
    
- 🧩 辅助编辑器 / 序列化 / 运行时行为
    

---

# 一、Inspector 显示 & 组织（最常用）

### ✅ `[Header]`

给字段加分组标题

```csharp
[Header("Combat Settings")]
public int damage;
public float cooldown;
```

👉 **几乎必用**

---

### ✅ `[Tooltip]`

鼠标悬停提示说明（给策划/未来的你）

```csharp
[Tooltip("Base damage before buffs")]
public int damage;
```

---

### ✅ `[Space]`

字段之间加空行

```csharp
public int a;

[Space(10)]
public int b;
```

---

### ✅ `[SerializeField]`

让 `private` 字段也能显示 & 序列化

```csharp
[SerializeField] private int hp;
```

👉 **Unity 项目里出现频率最高的标签之一**

---

### ⚠️ `[HideInInspector]`

序列化但不显示

```csharp
[HideInInspector]
public int runtimeValue;
```

📌 **数据还在，只是看不到**

---

# 二、数据合法性约束（强烈推荐）

### ✅ `[Range(min, max)]`

滑条限制数值范围

```csharp
[Range(0, 100)]
public int critRate;
```

👉 数值策划神器

---

### ✅ `[Min]`

保证最小值

```csharp
[Min(0)]
public int cost;
```

---

### ⚠️ `[Multiline]` / `[TextArea]`

多行字符串输入

```csharp
[TextArea(3, 6)]
public string description;
```

👉 用于**卡牌描述 / 任务文本**

---

# 三、引用安全 & 组件依赖（防 BUG）

### ✅ `[RequireComponent]`

**强制 GameObject 上必须有某组件**

```csharp
[RequireComponent(typeof(Rigidbody))]
public class Bullet : MonoBehaviour { }
```

👉 **防止运行时报 NullReferenceException**

---

### ✅ `[DisallowMultipleComponent]`

禁止重复添加组件

```csharp
[DisallowMultipleComponent]
public class GameManager : MonoBehaviour { }
```

---

### ⚠️ `[ExecuteAlways]`

编辑器 + 运行时都会执行

```csharp
[ExecuteAlways]
public class GridPreview : MonoBehaviour { }
```

❗ **谨慎使用，容易脏数据**

---

# 四、ScriptableObject & 架构相关（你很常用）

### ✅ `[CreateAssetMenu]`

允许右键创建 ScriptableObject

```csharp
[CreateAssetMenu(menuName = "Card/Card Data")]
public class CardData : ScriptableObject { }
```

👉 **数据驱动项目必备**

---

### ⚠️ `[FormerlySerializedAs]`

字段重命名不丢数据（救命用）

```csharp
[FormerlySerializedAs("oldName")]
public int newName;
```

👉 **重构时非常重要**

---

# 五、运行时 & 编译控制（进阶）

### ⚠️ `[RuntimeInitializeOnLoadMethod]`

**无需 MonoBehaviour，自动执行**

```csharp
[RuntimeInitializeOnLoadMethod]
static void Init()
{
    Debug.Log("Game Init");
}
```

👉 用于全局注册、配置初始化

---

### ⚠️ `[ContextMenu]`

右键执行函数（调试神器）

```csharp
[ContextMenu("Reset Data")]
void ResetData()
{
    hp = 100;
}
```

---

### ⚠️ `[Conditional("UNITY_EDITOR")]`

只在特定编译条件下生效

```csharp
[Conditional("UNITY_EDITOR")]
void DebugLog(string msg)
{
    Debug.Log(msg);
}
```

---

# 六、**强烈建议你优先掌握的 Top 10**

如果只记 10 个，记这几个 👇

1. `[SerializeField]`
    
2. `[Header]`
    
3. `[Tooltip]`
    
4. `[Range]`
    
5. `[Min]`
    
6. `[RequireComponent]`
    
7. `[DisallowMultipleComponent]`
    
8. `[CreateAssetMenu]`
    
9. `[FormerlySerializedAs]`
    
10. `[ContextMenu]`
