## C# `EventHandler` 核心笔记总结

### 一、`EventHandler` 是什么？

1. **定义：** `EventHandler` 是一个 **委托（Delegate）** 类型，它不是一个库，而是 **.NET 框架内置** 的核心组件。
    
2. **用途：** 专门用于 **定义和处理事件（Events）**，是 .NET 中事件处理的标准设计模式。
    
3. **特性：** `EventHandler` 委托的方法签名是**固定且规范化**的。
    

### 二、`EventHandler` 的标准签名

标准 `EventHandler` 委托要求处理方法遵循以下签名：

|参数|类型|作用|
|---|---|---|
|**返回值**|`void`|事件处理程序不应返回任何值。|
|**第一个参数**|`object? sender`|**事件的发送者**，即引发事件的对象实例（通常是 `this`）。|
|**第二个参数**|`EventArgs e`|**事件数据**。包含与事件相关的任何信息。|

### 三、泛型版本：`EventHandler<TEventArgs>`

当需要传递自定义事件数据时，应使用泛型版本：

C#

```
public delegate void EventHandler<TEventArgs>(object? sender, TEventArgs e)
    where TEventArgs : EventArgs;
```

- `TEventArgs`：必须是继承自 **`System.EventArgs`** 的自定义类，用于携带特定的事件信息（如新的分数、鼠标位置等）。
    

### 四、`EventArgs` 是什么？

`EventArgs` 是事件数据的基础。

1. **`System.EventArgs`：**
    
    - **基类**，自身不包含任何数据。
        
    - 作为所有事件数据类的 **标记**。
        
    - 当事件不需要任何数据时，使用静态实例 `EventArgs.Empty`。
        
2. **自定义数据：**
    
    - 如果需要传递数据，必须**继承** `EventArgs` 创建一个自定义类（如 `ScoreChangedEventArgs`）。
        
    - 将需要的数据作为属性或字段放在这个自定义类中。
        

### 五、与 `Action` 的关键区别（Action vs EventHandler）

|特性|**`EventHandler`**|**`Action`**|
|---|---|---|
|**角色定位**|遵循标准的 **事件处理模式**。|通用的 **无返回值委托/回调**。|
|**参数要求**|**强制** 包含 `sender` 和 `EventArgs`。|**灵活**，参数数量和类型可自由定义（0到16个）。|
|**数据传递**|通过 **`EventArgs` 对象** 打包传递数据。|通过 **独立参数** 传递数据。|
|**适用场景**|适用于公共 API、复杂事件或需要 `sender` 信息的场景。|适用于内部代码、Unity 等追求 **简洁高效** 的场景。|

**总结：** 在 C# 中，**`EventHandler`** 是定义事件的**规范做法**，提供了统一的签名和数据包装机制 (`EventArgs`)；而 **`Action`** 是一种**简洁替代方案**，更灵活地用于通用回调和简单的事件通知。