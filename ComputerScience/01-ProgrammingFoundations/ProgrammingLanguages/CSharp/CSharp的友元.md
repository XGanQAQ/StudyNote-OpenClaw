---
tags:
  - "#CSharp"
---

我们来详细聊聊C#中的“友元”这个概念。

首先，最重要的一点是：**C# 语言本身没有像 C++ 那样的 `friend` 关键字。**

C++ 中的 `friend` 允许一个类或函数访问另一个类的私有（`private`）和保护（`protected`）成员，这在某些情况下很方便，但也被认为在一定程度上破坏了类的封装性。C# 的设计者们出于对更强封装性和类型安全的考虑，没有引入这个特性。

然而，在实际开发中，我们确实会遇到类似的需求，比如：

- 一个类的内部逻辑非常复杂，需要拆分成多个辅助类，而这些辅助类需要访问主类的私有状态。
- 为某个程序集（Assembly）编写单元测试时，测试代码需要访问被测类的内部成员。

为了解决这些问题，C# 提供了几种替代方案，其中最接近“友元”概念的是 **`internal` 关键字** 和 **`InternalsVisibleToAttribute` 特性** 的组合。

### 1. 最接近的替代方案：`internal` 和 `InternalsVisibleToAttribute`

这个组合实现了 **“友元程序集”（Friend Assembly）** 的概念，它允许一个程序集（比如一个 `.dll` 文件）访问另一个程序集的 `internal` 成员。

#### a) `internal` 关键字

在 C# 中，`internal` 是一个访问修饰符。被 `internal` 修饰的类型或成员只能在**其所在的同一个程序集**内部被访问。你可以把它理解为“程序集级别的 `public`”。

示例：

假设我们有一个项目 MyLibrary，它会生成 MyLibrary.dll。

C#

```
// 在 MyLibrary.dll 项目中
namespace MyLibrary
{
    public class MyClass
    {
        // 这个方法只能在 MyLibrary.dll 内部被调用
        internal void DoSomethingInternal()
        {
            Console.WriteLine("这是一个内部方法。");
        }

        private void DoSomethingPrivate()
        {
            Console.WriteLine("这是一个私有方法。");
        }
    }
}
```

在 `MyLibrary` 项目的任何其他代码中，都可以调用 `DoSomethingInternal()`。但在项目外部（比如另一个引用了 `MyLibrary.dll` 的项目）是无法访问的。

#### b) `InternalsVisibleToAttribute` 特性

现在，如果我们想让一个特定的“朋友”程序集（比如我们的测试项目 `MyLibrary.Tests`）也能访问 `MyLibrary` 的 `internal` 成员，该怎么办？

这时 `InternalsVisibleToAttribute` 就派上用场了。你需要在**被访问**的程序集（`MyLibrary`）中添加这个特性，并指定“朋友”程序集的名称。

**操作步骤：**

1. **在 `MyLibrary` 项目中**，找到 `AssemblyInfo.cs` 文件（在旧版 .NET Framework 项目中），或者直接在任何一个 `.cs` 文件中（推荐在项目根目录新建一个文件如 `AssemblyAttributes.cs`）添加以下代码：
    
    C#
    
    ```
    // 在 MyLibrary 项目的某个 .cs 文件顶部，或者 AssemblyInfo.cs 中
    using System.Runtime.CompilerServices;
    
    // 将 MyLibrary 的 internal 成员对 "MyLibrary.Tests" 程序集可见
    [assembly: InternalsVisibleToAttribute("MyLibrary.Tests")]
    ```
    
    - **注意**：`"MyLibrary.Tests"` 是朋友程序集的**程序集名称**，而不是命名空间。如果朋友程序集是强签名的，这里还需要提供其公钥。
2. **在 `MyLibrary.Tests` 项目中**，你现在可以直接访问 `MyLibrary` 的 `internal` 成员了。
    
    C#
    
    ```
    // 在 MyLibrary.Tests.dll 项目中
    using MyLibrary;
    
    public class MyClassTests
    {
        public void TestInternalMethod()
        {
            MyClass instance = new MyClass();
    
            // 下面这行代码现在可以正常编译和运行了！
            instance.DoSomethingInternal(); 
    
            // 注意：私有成员依然无法访问
            // instance.DoSomethingPrivate(); // 这行代码会编译错误
        }
    }
    ```
    

总结：

这种方式是 C# 中实现类似“友元”功能最常用、最规范的方法。它在程序集级别上授予访问权限，非常适合用于单元测试或分离大型框架的内部实现和公共 API。

---

### 2. 其他替代模式

除了“友元程序集”，还有一些设计模式也能实现类似的效果，但应用场景不同。

#### a) 嵌套类（Nested Class）

一个类可以定义在另一个类的内部，这个内部类被称为嵌套类。嵌套类可以访问其外部类的所有成员，包括 `private` 成员。

当两个类的关系非常紧密，其中一个完全为另一个服务时，这是一个很好的选择。

**示例：**

C#

```
public class OuterClass
{
    private int _privateData = 42;
    private void PrivateMethod()
    {
        Console.WriteLine("外部类的私有方法。");
    }

    // 嵌套类
    public class NestedClass
    {
        public void AccessOuterMembers(OuterClass outer)
        {
            // 可以访问外部类的私有字段和方法
            Console.WriteLine($"访问外部类的私有数据: {outer._privateData}");
            outer.PrivateMethod();
        }
    }
}

// 使用方法
public class Demo
{
    public void Run()
    {
        OuterClass outerInstance = new OuterClass();
        OuterClass.NestedClass nestedInstance = new OuterClass.NestedClass();
        nestedInstance.AccessOuterMembers(outerInstance);
    }
}
```

#### b) 显式接口实现（Explicit Interface Implementation）

这是一种更精巧的控制访问权限的方法。你可以将需要特殊访问的成员定义在一个接口中，然后类通过**显式实现**这个接口来隐藏这些成员，只有通过接口的引用才能访问它们。

**示例：**

C#

```
// 1. 定义一个只有“朋友”才知道的“秘密”接口
public interface ISecretAccessor
{
    void PerformSecretOperation();
}

// 2. 类显式实现这个接口
public class MySecretiveClass : ISecretAccessor
{
    // 显式实现，这个方法不是 public 的
    void ISecretAccessor.PerformSecretOperation()
    {
        Console.WriteLine("执行秘密操作！");
    }

    public void DoPublicStuff()
    {
        Console.WriteLine("这是一个公共操作。");
    }
}

// 3. “朋友”类通过接口来访问
public class FriendClass
{
    public void WorkWithFriend(MySecretiveClass secret)
    {
        // 普通引用无法调用
        // secret.PerformSecretOperation(); // 编译错误

        // 将对象转换为接口类型，即可调用
        ISecretAccessor accessor = secret;
        accessor.PerformSecretOperation();
    }
}
```

### 总结对比

|   |   |   |   |   |
|---|---|---|---|---|
|**方法**|**粒度**|**优点**|**缺点**|**主要应用场景**|
|**`internal` + `InternalsVisibleTo`**|**程序集级别**|官方推荐，清晰明了，不破坏类的封装性（对外部世界而言）|授权范围是整个程序集，无法细化到单个类|**单元测试**、大型框架内部模块间协作|
|**嵌套类**|**类级别**|逻辑内聚性强，关系紧密，完全访问权限|增加了类的复杂性，只适用于“从属”关系|当一个类是另一个类的实现细节时|
|**显式接口实现**|**接口成员级别**|访问控制非常精细，符合面向接口编程思想|实现略复杂，需要传递接口引用|需要将特定功能暴露给特定消费者，同时对其他代码隐藏|

总而言之，虽然 C# 没有 `friend` 关键字，但它提供了更结构化、更安全的方式来解决类似的问题。在大多数情况下，**`InternalsVisibleToAttribute` 是你最需要了解和使用的“C#版友元”**。