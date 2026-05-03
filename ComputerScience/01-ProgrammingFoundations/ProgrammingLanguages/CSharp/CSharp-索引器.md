索引器是 **C#** 中的一个特殊功能，它允许您像使用数组一样，通过**索引**来访问类或结构体的实例。它让您的类看起来像一个“**智能数组**”或“**字典**”，从而提供更直观、更自然的访问方式。

---

## 索引器的基本概念和用途

### 1. 概念

索引器允许您使用方括号 `[]` 来访问对象中的数据，就像访问数组元素一样：

C#

```
MyObject obj = new MyObject();
// 使用索引器访问数据
string value = obj[index]; 
obj[index] = newValue;
```

索引器**不是静态成员**，它与实例关联。一个类可以定义多个不同参数类型的索引器（**重载**）。

### 2. 为什么使用索引器？

当您的类或结构体本质上是一个**集合（Collection）或列表（List）**，或者内部需要通过某种键（Key）或序号（Index）来查找和存储数据时，索引器就非常有用。

**典型应用场景：**

- **封装内部数组或列表：** 允许外部通过序号访问内部的集合数据，但又可以隐藏内部实现的细节。
    
- **实现类似字典的功能：** 允许您使用非整数类型（如 `string`）作为索引来查找数据（类似于 `Dictionary<TKey, TValue>`）。
    

---

## 索引器的语法结构

索引器的声明与属性（Property）非常相似，但有以下关键区别：

1. 它使用关键字 `this`。
    
2. 它在方括号 `[]` 内接受一个或多个**参数**。
    
3. 它没有名称。
    

C#

```
public class DataStore
{
    private string[] data = new string[10];

    // 索引器的声明
    public string this[int index] // 'this' 关键字和参数列表
    {
        // 类似于属性的 getter，用于获取值
        get 
        {
            // 确保索引有效
            if (index >= 0 && index < data.Length)
            {
                return data[index];
            }
            throw new IndexOutOfRangeException("索引超出范围。");
        }
        
        // 类似于属性的 setter，用于设置值
        set 
        {
            // 确保索引有效
            if (index >= 0 && index < data.Length)
            {
                data[index] = value; // 'value' 是隐式参数，代表要赋的新值
            }
            else
            {
                throw new IndexOutOfRangeException("索引超出范围。");
            }
        }
    }
}
```

### 示例用法：

C#

```
DataStore store = new DataStore();

// 设置值 (调用 set 访问器)
store[0] = "Hello C#";
store[1] = "Indexer";

// 获取值 (调用 get 访问器)
string item1 = store[0]; // item1 = "Hello C#"

Console.WriteLine(item1);
// Console.WriteLine(store[10]); // 这将抛出 IndexOutOfRangeException 异常
```

---

## 索引器的重要特性

### 1. 索引器重载

您可以为同一个类定义多个索引器，只要它们的**参数签名**（参数的数量和类型）不同即可。

**例如，一个使用 `int` 索引，另一个使用 `string` 索引：**

C#

```
public string this[int index] { /* ... */ } 
public string this[string key] { /* ... */ } // 像字典一样访问
```

### 2. 访问修饰符

索引器可以有自己的访问修饰符（`public`, `private`, `protected` 等），并且 `get` 和 `set` 访问器也可以有不同的访问修饰符，只要它们的限制性强于索引器本身的修饰符。

### 3. 表达式主体索引器（Expression-Bodied Indexers）

对于简单的 `get` 访问器，可以使用表达式主体语法（C# 6.0 及以上）：

C#

```
public string this[int index] => data[index]; // 仅有 get 访问器
```

或者同时包含 `get` 和 `set`（C# 7.0 及以上）：

C#

```
public string this[int index]
{
    get => data[index];
    set => data[index] = value;
}
```

---

## 总结

索引器是 **C# 语法糖**的一种体现，它提供了一种简洁、直观的方式来访问作为集合的类实例中的数据，使您的自定义类型更易于使用，尤其是在处理列表、数组或键值对数据时。

您想了解索引器在实际应用中的具体例子，比如如何用字符串作为索引键吗？