## Unity.Properties 是什么？

- Unity 提供的一套 **数据属性描述与访问库**
    
- 用于 **在不知道具体类型结构的情况下，统一、强类型地读写对象数据**
    
- 本质是 **Property + PropertyBag + Visitor** 的组合
    
- 主要服务于 **数据驱动、DOTS、编辑器与通用工具系统**
    

---

### 解决了什么问题

- ❌ 反射慢、不安全、AOT / Burst 不友好
    
- ❌ `SerializedProperty` 只能在编辑器使用，运行时不统一
    
- ❌ 通用工具（Inspector、Diff、批量修改）难以复用
    

**Unity.Properties 提供：**

- 无反射、强类型的数据访问
    
- 可遍历任意数据结构
    
- 编辑器 & 运行时统一的数据操作方式
    

---

## 如何使用的简单例子

```csharp
using Unity.Properties;

[GeneratePropertyBag]
struct PlayerData {
    public int Hp;
    public int Atk;
}
```

```csharp
struct PrintVisitor : IPropertyVisitor {
    public void Visit<TContainer, TValue>(
        Property<TContainer, TValue> property,
        ref TContainer container,
        ref TValue value)
    {
        Debug.Log(value);
    }
}
```

```csharp
var player = new PlayerData { Hp = 10, Atk = 5 };
PropertyContainer.Visit(ref player, new PrintVisitor());
```

效果：遍历并访问 `PlayerData` 的所有字段。

---

## 常见的 API

- `Property<TContainer, TValue>`  
    → 描述一个可访问的数据字段
    
- `PropertyBag<T>`  
    → 一个类型的所有 Property 的集合（自动生成）
    
- `PropertyContainer.Visit(ref T, IPropertyVisitor)`  
    → 访问任意类型的所有 Property
    
- `[GeneratePropertyBag]`  
    → 标记类型，生成对应的 PropertyBag
    
- `IPropertyVisitor`  
    → 编写通用的数据处理逻辑
    

---

### 一句话速记

> **Unity.Properties = 无反射 + Visitor 的数据访问系统，用来统一处理未知结构的数据。**