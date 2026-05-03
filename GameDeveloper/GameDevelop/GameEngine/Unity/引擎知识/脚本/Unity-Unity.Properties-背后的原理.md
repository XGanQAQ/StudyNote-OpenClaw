这是一个**非常好的“原理层”问题**，而且你已经在往 **Unity 架构 / 引擎内部思维** 靠拢了 👍  
我会把 **Unity.Properties 的“无反射”原理拆开讲清楚**，不靠黑箱。

---

# 一句话结论（先给结论）

> **Unity.Properties 的“无反射”，本质是：  
> 👉 用「源码生成 + 泛型 + 显式代码」  
> 👉 在编译期把“反射要做的事”提前写死成代码。**

不是“不用反射还能 magically 发现字段”，  
而是 **根本不需要发现 —— 因为早就生成好了**。

---

# 一、为什么反射能做这些事？

先回忆一下反射本来在干嘛：

- 找到一个类型有哪些字段
    
- 知道字段的类型
    
- 知道怎么 get / set
    
- 在运行时根据字符串访问
    

👉 **Unity.Properties 做的事完全一样，只是时机不同**。

---

# 二、Unity.Properties 的核心思路

## 1️⃣ 编译期生成 PropertyBag（关键）

```csharp
[GeneratePropertyBag]
struct PlayerData {
    public int Hp;
    public int Atk;
}
```

当你写下这行代码时：

👉 **Unity 的 Source Generator 会在编译期生成代码**

类似这样（概念化示意）：

```csharp
class PlayerData_PropertyBag : PropertyBag<PlayerData> {
    public PlayerData_PropertyBag() {
        AddProperty(new HpProperty());
        AddProperty(new AtkProperty());
    }
}
```

---

## 2️⃣ 每个字段 = 一个强类型 Property

```csharp
class HpProperty : Property<PlayerData, int> {
    public override int GetValue(ref PlayerData container)
        => container.Hp;

    public override void SetValue(ref PlayerData container, int value)
        => container.Hp = value;
}
```

注意这里非常重要的几点：

- ✔ **没有字符串**
    
- ✔ **没有反射**
    
- ✔ **是普通的 C# 代码**
    
- ✔ **泛型类型在编译期就确定**
    

👉 **这就是“反射能力被翻译成代码”的地方**

---

# 三、PropertyContainer 是怎么找到这些 Property 的？

你会疑惑：

> 「那 `PropertyContainer.Visit(ref obj)` 怎么知道用哪个 PropertyBag？」

答案是：**泛型 + 静态注册**

---

## 1️⃣ 每个类型在第一次使用时注册 PropertyBag

概念示意：

```csharp
static class PropertyBagStore<T> {
    public static readonly PropertyBag<T> Bag = new PlayerData_PropertyBag();
}
```

当你调用：

```csharp
PropertyContainer.Visit(ref player, visitor);
```

编译器已经知道：

- `T = PlayerData`
    
- `PropertyBag<PlayerData>` 是什么
    

👉 **没有任何运行时类型判断**

---

## 2️⃣ 泛型消除了反射需求

```csharp
Visit<T>(ref T container, IPropertyVisitor visitor)
```

- `T` 在编译期确定
    
- PropertyBag 在编译期绑定
    
- 字段访问是普通函数调用
    

👉 **IL2CPP / AOT / Burst 都完全 OK**

---

# 四、Visitor 为什么也不需要反射？

Visitor 的核心接口是：

```csharp
Visit<TContainer, TValue>(
    Property<TContainer, TValue> property,
    ref TContainer container,
    ref TValue value)
```

### 关键点：

- `TValue` 是真实类型（int / float / struct）
    
- 不用 `object`
    
- 不用 `Type`
    
- 不用 `switch`
    

👉 编译器已经帮你分发好了。

这其实是 **Visitor Pattern + 泛型** 的威力。

---

# 五、对比反射 VS Unity.Properties（核心差异）

|维度|反射|Unity.Properties|
|---|---|---|
|发现字段|运行时|编译期|
|字段名|string|强类型|
|Get / Set|FieldInfo|直接代码|
|性能|慢|接近手写|
|AOT / Burst|❌|✅|
|错误发现|运行时|编译期|

---

# 六、那为什么 Unity 要这么“麻烦”？

因为 Unity 要解决的是：

- DOTS
    
- ECS
    
- IL2CPP
    
- 跨平台
    
- 编辑器 + 运行时统一
    

👉 **反射在这些场景下几乎全是雷**

Unity.Properties 是 **Unity 内部系统级基础设施**。

---

# 七、用一句话把“原理”记住（笔记级）

> **Unity.Properties 不是“不用反射还能反射”，  
> 而是用 Source Generator 在编译期生成  
> PropertyBag 和 Property 的显式代码，  
> 再用泛型 + Visitor 在运行时高效遍历数据。**
