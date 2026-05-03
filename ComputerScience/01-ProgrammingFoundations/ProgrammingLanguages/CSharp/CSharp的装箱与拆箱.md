---
tags:
  - "#CSharp"
---

在 C# 中，**装箱和拆箱是与值类型（Value Types）和引用类型（Reference Types）之间的转换相关的概念。简单来说，它们允许你在需要时将值类型转换为引用类型，然后再转换回来。**

### 1. 什么是装箱 (Boxing)？

装箱是将**值类型**的实例隐式或显式地转换为**引用类型**（通常是 `object` 类型或由 `System.ValueType` 派生而来的接口类型）的过程。

当一个值类型被装箱时，以下事情会发生：

1. **内存分配：** 在托管堆上分配内存，以存储值类型的副本。
2. **数据复制：** 值类型实例的实际值被复制到新分配的堆内存中。
3. **引用返回：** 返回一个引用，指向堆上新创建的对象。

**示例：**

```csharp
int num = 123; // 值类型
object obj = num; // 装箱：num 的值被复制到堆上，obj 引用该堆对象

Console.WriteLine($"num 的类型: {num.GetType()}"); // 输出 System.Int32
Console.WriteLine($"obj 的类型: {obj.GetType()}"); // 输出 System.Int32 (虽然它现在是 object 类型，但其底层类型仍然是 Int32)
Console.WriteLine($"num 的值: {num}"); // 输出 123
Console.WriteLine($"obj 的值: {obj}"); // 输出 123
```

**什么时候会发生装箱？**

- 将值类型赋值给 `object` 类型的变量时。
- 将值类型赋值给 `System.ValueType` 派生而来的接口类型的变量时。
- 将值类型作为参数传递给期望 `object` 类型或接口类型的方法时（例如，`Console.WriteLine()`）。
- 将值类型放入非泛型集合（如 `ArrayList`）时。

### 2. 什么是拆箱 (Unboxing)？

拆箱是从**引用类型**（通常是 `object` 类型）显式地转换回**值类型**的过程。

当一个对象被拆箱时，以下事情会发生：

1. **类型检查：** 首先，运行时会检查引用对象是否是指定值类型的**装箱版本**。如果不是，会抛出 `InvalidCastException` 异常。
2. **数据复制：** 如果类型匹配，将堆上存储的值复制回栈上的值类型变量。

**示例：**

```C#
int num = 123; // 值类型
object obj = num; // 装箱

// 拆箱：将 obj 显式转换为 int 类型
// 注意：这里必须进行显式类型转换 (int)
int unboxedNum = (int)obj;

Console.WriteLine($"unboxedNum 的类型: {unboxedNum.GetType()}"); // 输出 System.Int32
Console.WriteLine($"unboxedNum 的值: {unboxedNum}"); // 输出 123
```

**拆箱的注意事项：**

- **必须是显式转换：** 拆箱操作必须是显式的，不能隐式进行。
    
- **类型匹配：** 拆箱时，目标值类型必须与被装箱前的原始值类型完全匹配。例如，你不能将一个装箱的 `int` 拆箱为 `long`。
    
    
    ```C#
    object obj = 123; // int 被装箱
    // long wrongNum = (long)obj; // 这会抛出 InvalidCastException，因为 obj 存储的是 int 而不是 long
    ```
    

### 3. 装箱与拆箱的性能影响

装箱和拆箱操作会带来一定的性能开销，主要体现在以下几个方面：

- **内存分配：** 装箱需要在堆上分配新的内存。
- **数据复制：** 涉及值类型数据从栈到堆（装箱）或从堆到栈（拆箱）的复制。
- **垃圾回收：** 堆上分配的对象最终需要被垃圾回收器处理，这会增加 GC 的压力。
- **类型检查：** 拆箱时需要进行运行时类型检查。

因此，在编写高性能代码时，应尽量避免不必要的装箱和拆箱操作。

### 4. 泛型 (Generics) 如何避免装箱与拆箱？

泛型是 C# 2.0 引入的一个重要特性，它在很大程度上解决了非泛型集合（如 `ArrayList`）中值类型装箱和拆箱带来的性能问题。

使用泛型集合（如 `List<T>`、`Dictionary<TKey, TValue>`）时，类型参数 `T` 在编译时就确定了，因此编译器知道集合中存储的确切类型。这样，值类型可以直接存储在泛型集合中，而无需进行装箱。

**示例：**


```C#
// 使用非泛型集合，会导致装箱
System.Collections.ArrayList arrayList = new System.Collections.ArrayList();
arrayList.Add(1); // 1 (int) 被装箱

// 使用泛型集合，不会导致装箱
System.Collections.Generic.List<int> intList = new System.Collections.Generic.List<int>();
intList.Add(1); // 1 (int) 直接存储，没有装箱
```

### 总结

- **装箱 (Boxing)：** 将**值类型**转换为**引用类型**。是隐式或显式的。
- **拆箱 (Unboxing)：** 将**引用类型**显式转换回**值类型**。必须是显式的，且类型必须精确匹配。
- **性能开销：** 装箱和拆箱会引入内存分配、数据复制和垃圾回收的开销，应尽量避免。
- **泛型：** 使用泛型集合是避免值类型装箱和拆箱的最佳实践。

理解装箱和拆箱对于编写高效和正确的 C# 代码非常重要。希望这个解释对你有帮助！