---
tags:
  - "#CSharp"
---

### C# 委托（Delegate）介绍

在 C# 中，**委托（Delegate）** 是一种**类型安全的函数指针**，它允许你将方法作为参数传递，或者将方法赋值给变量。委托可以引用一个或多个方法，并且可以在运行时动态地调用这些方法。委托是 C# 中实现事件、回调机制以及异步编程的基础。

#### 委托的基本概念

1. **定义委托**：
   委托是一种引用类型，使用 `delegate` 关键字定义。委托的签名（即方法的参数列表和返回类型）必须与它引用的方法一致。

   ```csharp
   public delegate void MyDelegate(string message);
   ```

   上面的代码定义了一个名为 `MyDelegate` 的委托，它可以引用任何接受一个 `string` 参数并返回 `void` 的方法。

2. **创建委托实例**：
   你可以将符合委托签名的方法赋值给委托实例。

   ```csharp
   public void DisplayMessage(string message)
   {
       Console.WriteLine(message);
   }

   MyDelegate myDelegate = new MyDelegate(DisplayMessage);
   ```

3. **调用委托**：
   通过委托实例可以调用它所引用的方法。

   ```csharp
   myDelegate("Hello, World!");
   ```

4. **多播委托**：
   委托可以引用多个方法，这种委托称为多播委托。调用多播委托时，所有引用的方法都会被依次调用。

   ```csharp
   MyDelegate myDelegate = DisplayMessage;
   myDelegate += AnotherMethod;
   myDelegate("Hello, World!"); // 调用 DisplayMessage 和 AnotherMethod
   ```

5. **事件**：
   委托是事件的基础。事件是一种特殊的委托，它封装了委托的调用，防止外部代码直接调用委托。

   ```csharp
   public event MyDelegate MyEvent;

   protected virtual void OnMyEvent(string message)
   {
       MyEvent?.Invoke(message);
   }
   ```

### 委托的实现原理

委托的实现原理涉及到 C# 的类型系统和运行时机制。以下是委托的核心实现原理：

1. **委托类型**：
   委托类型在编译时被定义为一个类，这个类继承自 `System.MulticastDelegate`。`MulticastDelegate` 是所有委托的基类，它提供了委托的核心功能。

   ```csharp
   public sealed class MyDelegate : MulticastDelegate
   {
       // 构造函数
       public MyDelegate(object target, IntPtr method);

       // 调用方法
       public virtual void Invoke(string message);

       // 异步调用方法
       public virtual IAsyncResult BeginInvoke(string message, AsyncCallback callback, object state);

       // 结束异步调用方法
       public virtual void EndInvoke(IAsyncResult result);
   }
   ```

2. **委托实例**：
   当你创建一个委托实例时，实际上是在创建一个 `MulticastDelegate` 的子类实例。这个实例包含两个关键信息：
   • **目标对象（Target）**：委托所引用的方法所属的对象实例。如果是静态方法，目标对象为 `null`。
   • **方法指针（MethodPtr）**：指向目标方法的指针。

3. **委托调用**：
   当你调用委托时，实际上是通过 `Invoke` 方法来执行的。`Invoke` 方法会根据目标对象和方法指针，通过反射机制调用目标方法。

   ```csharp
   myDelegate("Hello, World!");
   ```

   这行代码实际上等价于：

   ```csharp
   myDelegate.Invoke("Hello, World!");
   ```

4. **多播委托的实现**：
   多播委托内部维护了一个 `InvocationList`，它是一个委托链表。当你将多个委托相加时，实际上是将它们添加到这个链表中。调用多播委托时，会依次调用链表中的每个委托。

   ```csharp
   myDelegate += AnotherMethod;
   ```

   调用 `myDelegate` 时，会依次调用 `DisplayMessage` 和 `AnotherMethod`。

5. **异步调用**：
   委托还支持异步调用，通过 `BeginInvoke` 和 `EndInvoke` 方法实现。异步调用会将方法的执行放到线程池中，并在方法执行完成后通过回调函数通知调用者。

### 总结

C# 委托是一种强大的机制，它允许你将方法作为参数传递、实现回调、事件处理以及异步编程。委托的实现原理基于 `MulticastDelegate` 类，它通过维护目标对象和方法指针来实现方法的调用。多播委托通过委托链表实现多个方法的依次调用，而异步调用则通过线程池和回调机制实现。

理解委托的工作原理对于掌握 C# 中的事件驱动编程、异步编程以及函数式编程非常重要。