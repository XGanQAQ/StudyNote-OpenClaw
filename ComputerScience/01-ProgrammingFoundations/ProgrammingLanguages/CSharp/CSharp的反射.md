---
tags:
  - "#CSharp"
---
### 什么是 C# 反射？

在 C# 中，反射是指程序在运行时检查自身或其它程序集（Assembly）的元数据（Metadata）的能力。简单来说，它允许你在运行时动态地获取类型信息、构造对象、调用方法、访问字段和属性等，而不需要在编译时就知道这些信息的具体细节。

这就像给你的程序安装了一双“透视眼”，让它在运行时也能看清楚自己内部的结构。

### 反射的主要用途和场景

反射在许多高级和框架级的场景中都非常有用，例如：

1. **动态加载和调用：**
    
    - **插件系统：** 许多应用程序支持插件。通过反射，应用程序可以动态加载插件程序集，发现其中实现了特定接口或继承了特定基类的类型，并创建它们的实例。
    - **延迟加载：** 当你需要直到运行时才能确定要使用的类型时。
2. **构建通用库和框架：**
    
    - **ORM (Object-Relational Mapping) 框架：** 如 Entity Framework，它使用反射来将数据库中的数据映射到 C# 对象，或将 C# 对象映射到数据库表。
    - **序列化和反序列化：** JSON.NET 或 XML 序列化器使用反射来遍历对象的属性并将其转换为字符串，或将字符串解析回对象。
    - **依赖注入 (DI) 容器：** 它们使用反射来发现构造函数、方法和属性，以便在创建对象时注入依赖项。
3. **特性 (Attributes) 的使用：**
    
    - 反射是读取和处理自定义特性（Attribute）的关键。你可以定义自己的特性来标记代码元素（类、方法、属性等），然后在运行时通过反射检查这些特性并执行相应的逻辑。例如，ASP.NET MVC/Core 中的路由特性、授权特性等。
4. **元数据检查：**
    
    - **开发工具和IDE：** Visual Studio 等工具使用反射来显示类型信息、方法签名、属性等，以提供智能感知。
    - **单元测试框架：** 如 NUnit 或 xUnit，它们使用反射来发现和执行测试方法。
5. **代码生成和动态代理：**
    
    - 在某些高级场景中，你可以使用反射结合 `System.Reflection.Emit` 命名空间来在运行时生成新的代码。

### 反射的核心类

C# 反射主要通过 `System.Reflection` 命名空间中的类来实现：

- **`Assembly`：** 代表一个程序集。你可以加载程序集，并从中获取其中定义的类型。
- **`Type`：** 最核心的类，代表一个类型（类、接口、结构、枚举、委托等）。你可以通过它获取类型的名称、基类、接口、成员（方法、属性、字段、事件等）。
- **`MemberInfo`：** 这是一个抽象基类，表示一个成员（方法、属性、字段、事件或构造函数）。
- **`MethodInfo`：** 代表一个方法。你可以通过它获取方法的参数、返回类型，并调用方法。
- **`PropertyInfo`：** 代表一个属性。你可以通过它获取属性的类型，以及读取或设置属性的值。
- **`FieldInfo`：** 代表一个字段。你可以通过它获取字段的类型，以及读取或设置字段的值。
- **`ConstructorInfo`：** 代表一个构造函数。你可以通过它创建类型的实例。
- **`ParameterInfo`：** 代表一个方法的参数。

### 反射的基本操作示例

#### 1. 获取类型信息

C#

```
using System;
using System.Reflection;

public class MyClass
{
    public int MyProperty { get; set; }
    public string MyField = "Hello";

    public void MyMethod(string message)
    {
        Console.WriteLine($"Method called with: {message}");
    }
}

public class ReflectionExample
{
    public static void Main(string[] args)
    {
        // 方式一：使用 typeof 运算符获取类型信息（编译时已知类型）
        Type type1 = typeof(MyClass);
        Console.WriteLine($"Type Name (typeof): {type1.FullName}");

        // 方式二：使用 GetType() 方法获取实例的类型信息（运行时获取）
        MyClass myInstance = new MyClass();
        Type type2 = myInstance.GetType();
        Console.WriteLine($"Type Name (GetType()): {type2.FullName}");

        // 方式三：使用 Type.GetType() 方法根据类型名称获取类型信息
        // 注意：这里需要完整的命名空间和程序集名称（如果是不同的程序集）
        Type type3 = Type.GetType("MyClass"); // 如果在同一程序集下，直接类名即可
        if (type3 != null)
        {
            Console.WriteLine($"Type Name (Type.GetType()): {type3.FullName}");
        }

        // 获取类型的所有公共成员
        Console.WriteLine("\nPublic Members:");
        foreach (MemberInfo member in type1.GetMembers())
        {
            Console.WriteLine($"- {member.MemberType}: {member.Name}");
        }

        // 获取类型的所有公共属性
        Console.WriteLine("\nPublic Properties:");
        foreach (PropertyInfo prop in type1.GetProperties())
        {
            Console.WriteLine($"- Property: {prop.Name}, Type: {prop.PropertyType.Name}");
        }

        // 获取类型的所有公共方法
        Console.WriteLine("\nPublic Methods:");
        foreach (MethodInfo method in type1.GetMethods())
        {
            Console.WriteLine($"- Method: {method.Name}, Return Type: {method.ReturnType.Name}");
        }
    }
}
```

#### 2. 动态创建对象

C#

```
using System;
using System.Reflection;

public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public Person() { } // 无参构造函数

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public void SayHello()
    {
        Console.WriteLine($"Hello, my name is {Name} and I am {Age} years old.");
    }
}

public class DynamicObjectCreation
{
    public static void Main(string[] args)
    {
        Type personType = typeof(Person);

        // 方式一：使用 Activator.CreateInstance() 调用无参构造函数
        Person p1 = (Person)Activator.CreateInstance(personType);
        p1.Name = "Alice";
        p1.Age = 30;
        p1.SayHello();

        // 方式二：使用 Activator.CreateInstance() 调用带参构造函数
        Person p2 = (Person)Activator.CreateInstance(personType, "Bob", 25);
        p2.SayHello();

        // 方式三：获取特定构造函数并调用
        ConstructorInfo constructor = personType.GetConstructor(new Type[] { typeof(string), typeof(int) });
        if (constructor != null)
        {
            Person p3 = (Person)constructor.Invoke(new object[] { "Charlie", 40 });
            p3.SayHello();
        }
    }
}
```

#### 3. 动态调用方法

C#

```
using System;
using System.Reflection;

public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    private string GetSecretMessage()
    {
        return "This is a secret message.";
    }
}

public class DynamicMethodInvocation
{
    public static void Main(string[] args)
    {
        Calculator calc = new Calculator();
        Type calcType = typeof(Calculator);

        // 获取公共方法并调用
        MethodInfo addMethod = calcType.GetMethod("Add");
        if (addMethod != null)
        {
            object result = addMethod.Invoke(calc, new object[] { 10, 20 });
            Console.WriteLine($"Result of Add(10, 20): {result}");
        }

        // 获取私有方法并调用 (需要 BindingFlags.NonPublic 和 BindingFlags.Instance)
        MethodInfo secretMethod = calcType.GetMethod("GetSecretMessage", BindingFlags.NonPublic | BindingFlags.Instance);
        if (secretMethod != null)
        {
            object secretResult = secretMethod.Invoke(calc, null); // 私有方法通常没有参数
            Console.WriteLine($"Secret Message: {secretResult}");
        }
    }
}
```

#### 4. 动态访问属性和字段

C#

```
using System;
using System.Reflection;

public class Product
{
    public string Name { get; set; }
    public decimal Price;
    private int _stockQuantity; // 私有字段

    public Product(string name, decimal price, int stock)
    {
        Name = name;
        Price = price;
        _stockQuantity = stock;
    }

    public int GetStock()
    {
        return _stockQuantity;
    }
}

public class DynamicMemberAccess
{
    public static void Main(string[] args)
    {
        Product product = new Product("Laptop", 1200.50m, 50);
        Type productType = typeof(Product);

        // 动态访问和设置公共属性
        PropertyInfo nameProperty = productType.GetProperty("Name");
        if (nameProperty != null)
        {
            Console.WriteLine($"Original Name: {nameProperty.GetValue(product)}");
            nameProperty.SetValue(product, "Gaming Laptop");
            Console.WriteLine($"New Name: {nameProperty.GetValue(product)}");
        }

        // 动态访问和设置公共字段
        FieldInfo priceField = productType.GetField("Price");
        if (priceField != null)
        {
            Console.WriteLine($"Original Price: {priceField.GetValue(product)}");
            priceField.SetValue(product, 1500.00m);
            Console.WriteLine($"New Price: {priceField.GetValue(product)}");
        }

        // 动态访问私有字段 (需要 BindingFlags.NonPublic 和 BindingFlags.Instance)
        FieldInfo stockField = productType.GetField("_stockQuantity", BindingFlags.NonPublic | BindingFlags.Instance);
        if (stockField != null)
        {
            Console.WriteLine($"Original Stock: {stockField.GetValue(product)}");
            stockField.SetValue(product, 45);
            Console.WriteLine($"New Stock (via reflection): {stockField.GetValue(product)}");
            Console.WriteLine($"New Stock (via method): {product.GetStock()}"); // 验证
        }
    }
}
```

### 反射的优缺点

**优点：**

- **灵活性和扩展性：** 允许在运行时动态地发现和操作类型，这对于构建可扩展的、插件化的系统至关重要。
- **代码解耦：** 降低了硬编码的依赖，提高了模块的独立性。
- **元数据访问：** 能够读取和处理代码中的元数据，包括自定义特性。

**缺点：**

- **性能开销：** 相较于直接调用，反射操作通常更慢，因为它涉及到更多的运行时检查和查找。对于性能敏感的代码路径，应谨慎使用。
- **复杂性：** 反射的代码通常比直接操作的代码更复杂，可读性较低，也更容易出错（例如，如果调用的方法名或参数类型不匹配，会在运行时抛出异常）。
- **编译时检查缺失：** 反射绕过了编译时类型检查，这意味着一些本来可以在编译时发现的错误（如方法名拼写错误）可能会推迟到运行时才暴露，增加了调试难度。
- **安全限制：** 在某些受限的环境中（如 .NET Core 的某些裁剪模式），反射功能可能会受到限制。

### 总结

C# 反射是一个强大而高级的特性，它为程序在运行时检查和操作自身提供了无限可能。虽然它带来了性能和复杂性上的权衡，但在需要高度灵活性、可扩展性和通用性的场景中，反射是不可或缺的工具。理解反射的工作原理和适用场景，能让你在开发更高级的 C# 应用程序时游刃有余。