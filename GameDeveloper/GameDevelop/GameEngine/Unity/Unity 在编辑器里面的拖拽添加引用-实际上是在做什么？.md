## 1️⃣ 本质：给字段赋一个“对象引用”

当你写这样的代码：

```csharp
public GameObject target;
```

Unity 会把这个字段序列化（前提是它是可序列化的类型，比如 `public` 或 `[SerializeField]`）。

👉 当你在 Inspector 里拖一个对象进去时，Unity 实际做的是：

> 把这个对象的“引用”赋值给这个字段

类似于代码里的：

```csharp
target = someGameObject;
```

---

## 2️⃣ 引用到底是什么？

Unity 里的引用不是简单的内存地址，而是：

- 对于 **场景中的对象（Scene Object）**
    
    - 记录一个内部 ID（Instance ID / FileID）
        
- 对于 **资源（Asset，比如 Prefab、材质）**
    
    - 记录 GUID（资源唯一标识）+ FileID
        

也就是说：

> Inspector 里拖拽 = 存储一个可以“重新找到这个对象”的标识

---

## 3️⃣ 序列化系统在背后做的事

Unity 使用自己的序列化系统（不是标准 C# 序列化）。

当你拖拽时：

1. Inspector 检测到拖入对象类型匹配
    
2. 把该对象转换成序列化数据（ID/GUID）
    
3. 写入：
    
    - 场景文件（.unity）
        
    - 或 Prefab 文件（.prefab）
        

例如（简化理解）：

```yaml
target:
  fileID: 123456
  guid: abcdef123456...
```

---

## 4️⃣ 运行时如何恢复？

当你点击 Play：

1. Unity 加载场景
    
2. 反序列化这些字段
    
3. 根据 GUID / fileID 找到真实对象
    
4. 把引用重新绑定
    

👉 所以你的脚本里 `target` 就已经有值了

---

## 5️⃣ 为什么有时拖不进去？

因为 Unity 会做类型检查：

```csharp
public Rigidbody rb;
```

你只能拖：

- 有 Rigidbody 的对象
    
- 或直接拖组件本身
    

否则会被拒绝（类型不兼容）

---

## 6️⃣ 常见坑（本质原因）

### ❌ 拖了但运行时报 null

原因可能是：

- Prefab override 被覆盖
    
- 场景对象引用在 Prefab 中丢失（Prefab 不能引用场景对象）
    

---

### ❌ Prefab 不能引用 Scene 对象

因为：

> Prefab 是资产（Asset），不能依赖具体场景实例

---

## 7️⃣ 总结一句话

👉 Unity 的拖拽本质是：

> **通过序列化系统，把一个对象的“可追踪标识”写入字段，从而在运行时恢复引用**
