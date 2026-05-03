C# 中的对象初始化语法是一种方便的构造，它允许您在创建对象的同时为其公共属性或字段赋值，而无需显式调用构造函数并逐个设置属性。

---

### 工作原理

对象初始化器通过以下步骤工作：

1. **调用无参构造函数：** 首先，它会调用对象的默认（无参）构造函数。如果类没有显式定义无参构造函数，C# 编译器会自动提供一个。
    
2. **赋值属性/字段：** 接下来，它会按照您在初始化器中指定的顺序，为对象的公共属性或字段赋值。
    

---

### 语法

基本的对象初始化语法如下所示：

C#

```
var 对象名 = new 类名
{
    属性1 = 值1,
    属性2 = 值2,
    // ...
    属性N = 值N
};
```

- `对象名`：您要创建的对象的名称。
    
- `类名`：您要实例化的类的名称。
    
- `属性1 = 值1, ...`：这是一个逗号分隔的列表，其中包含您要设置的属性或字段以及它们对应的值。
    

---

### 示例

让我们通过一个简单的 `Person` 类来理解：

C#

```
public class Person
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public int Age { get; set; }

    // 您可以有其他构造函数，但对象初始化器会使用无参构造函数
    public Person()
    {
        Console.WriteLine("Person 的无参构造函数被调用。");
    }

    public Person(string firstName, string lastName)
    {
        FirstName = firstName;
        LastName = lastName;
        Console.WriteLine("Person 的带参数构造函数被调用。");
    }
}
```

**使用对象初始化器：**

C#

```
using System;

public class Program
{
    public static void Main(string[] args)
    {
        // 使用对象初始化器创建 Person 对象
        var person1 = new Person
        {
            FirstName = "张",
            LastName = "三",
            Age = 30
        };

        Console.WriteLine($"姓名：{person1.FirstName} {person1.LastName}, 年龄：{person1.Age}");

        // 也可以不设置所有属性
        var person2 = new Person
        {
            FirstName = "李",
            LastName = "四"
        };
        Console.WriteLine($"姓名：{person2.FirstName} {person2.LastName}, 年龄：{person2.Age}"); // Age 将为默认值 0

        // 与传统方式的对比
        Person person3 = new Person(); // 调用无参构造函数
        person3.FirstName = "王";
        person3.LastName = "五";
        person3.Age = 25;
        Console.WriteLine($"姓名：{person3.FirstName} {person3.LastName}, 年龄：{person3.Age}");
    }
}
```

**输出：**

```
Person 的无参构造函数被调用。
姓名：张 三, 年龄：30
Person 的无参构造函数被调用。
姓名：李 四, 年龄：0
Person 的无参构造函数被调用。
姓名：王 五, 年龄：25
```

从输出中可以看出，每次使用对象初始化器时，`Person` 类的无参构造函数都会被调用。

---

### 何时使用对象初始化器？

- **简化代码：** 当您需要创建对象并立即设置其多个属性时，它使代码更简洁、更易读。
    
- **创建临时对象：** 当您需要一个短生命周期的对象，不需要复杂的初始化逻辑时，非常方便。
    
- **LINQ 查询：** 在 LINQ 查询中创建匿名类型时经常使用。
    
- **集合初始化器：** 可以与集合初始化器结合使用，例如在初始化 `List<T>` 时。
    

---

### 限制和注意事项

- **只适用于可访问的成员：** 您只能初始化公共属性或公共字段。私有成员无法通过对象初始化器直接设置。
    
- **无参构造函数：** 对象初始化器始终首先调用无参构造函数。如果您的类只有一个带参数的构造函数而没有无参构造函数，那么您就不能直接使用对象初始化器。您需要提供一个无参构造函数，或者使用带参数的构造函数来创建对象，然后再逐个设置其余属性。
    
- **不是构造函数的替代品：** 对象初始化器并不是构造函数的替代品。构造函数用于执行更复杂的初始化逻辑，例如验证输入、设置只读属性或执行其他依赖项注入。对象初始化器只是语法糖，用于在对象创建后方便地赋值。
    
- **只读属性：** 您不能使用对象初始化器来设置只读属性（只有 `get` 访问器的属性），因为它们在对象创建后不能被修改。除非该属性在构造函数中被赋值。
    

总的来说，C# 的对象初始化语法是一个非常实用的功能，可以大大提高代码的简洁性和可读性，特别是在创建数据传输对象（DTO）或简单的实体类时。