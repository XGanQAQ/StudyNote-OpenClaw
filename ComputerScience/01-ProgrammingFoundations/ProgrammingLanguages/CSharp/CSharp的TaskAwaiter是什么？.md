---
tags:
  - "#CSharp"
---

在 C# 中，`TaskAwaiter` 是 `async` 和 `await` 机制的核心组成部分，但它通常不是我们直接使用的类型。它是一种编译器生成的结构体，用于支持 `await` 关键字的操作。

简单来说，当你使用 `await` 关键字等待一个 `Task`（或任何实现了“awaitable”模式的类型）时，编译器会在幕后将其转换为对 `TaskAwaiter` 实例的调用。

以下是 `TaskAwaiter` 的关键作用和特性：

1. **Awaits Task Completion（等待任务完成）**: `TaskAwaiter` 的主要职责是等待关联的异步 `Task` 完成。一旦 `Task` 完成（无论是成功、失败还是取消），`TaskAwaiter` 就会通知等待它的代码继续执行。
    
2. **获取结果（GetResult()）**: 如果 `Task` 有返回值（例如 `Task<TResult>`），`TaskAwaiter<TResult>` 会提供一个 `GetResult()` 方法。当 `Task` 完成后，调用 `GetResult()` 方法会返回 `Task` 的最终结果。如果 `Task` 抛出了异常，`GetResult()` 也会重新抛出该异常。对于 `Task`（没有返回值），`GetResult()` 方法是 `void` 类型的。
    
3. **检查完成状态（IsCompleted）**: `TaskAwaiter` 包含一个 `IsCompleted` 属性，用于指示关联的 `Task` 是否已经完成。如果 `Task` 在 `await` 表达式执行时就已经完成，那么 `await` 表达式会立即继续执行，而不会进行上下文切换。
    
4. **注册延续（OnCompleted/UnsafeOnCompleted）**: `TaskAwaiter` 还提供了 `OnCompleted` 和 `UnsafeOnCompleted` 方法。这些方法用于注册一个“延续”（continuation）操作，即当 `Task` 完成时需要执行的代码。`await` 关键字正是利用这些方法来安排在异步操作完成后执行 `await` 之后的代码。
    
5. **编译器魔法（Compiler Magic）**: `TaskAwaiter` 是 `async/await` 语法糖的幕后英雄。当你编写 `await someTask;` 时，C# 编译器会将其转换为类似以下的操作：
    
    C#
    
    ```
    var awaiter = someTask.GetAwaiter(); // 获取 Task 的 Awaiter
    if (!awaiter.IsCompleted)
    {
        // 如果 Task 未完成，注册一个延续
        // 这会捕获当前上下文（例如 UI 线程上下文或 ASP.NET 请求上下文），并在 Task 完成后回到这个上下文执行后续代码
        awaiter.OnCompleted(() =>
        {
            // 在 Task 完成后，调用 GetResult() 获取结果或重新抛出异常
            awaiter.GetResult();
            // 继续执行 await 表达式之后的代码
            // ...
        });
        // 挂起当前方法，并将控制权返回给调用方
        return;
    }
    else
    {
        // 如果 Task 已经完成，直接获取结果并继续执行
        awaiter.GetResult();
        // 继续执行 await 表达式之后的代码
        // ...
    }
    ```
    
    这个过程涉及到状态机的生成，编译器将 `async` 方法分解为多个部分，并在 `await` 处暂停执行，然后在 `Task` 完成时恢复执行。
    

**为什么我们通常不直接使用 `TaskAwaiter`？**

`TaskAwaiter` 位于 `System.Runtime.CompilerServices` 命名空间下，这表明它是一个主要供编译器内部使用的类型。直接使用 `TaskAwaiter` 会使代码变得复杂，并且通常没有必要。`async/await` 关键字提供了一个更简洁、更易读的方式来处理异步编程。

**总结：**

`TaskAwaiter` 是 C# 中 `async/await` 模式的一个底层构建块，它实现了“awaitable”模式所需的方法 (`GetResult()`、`IsCompleted` 和 `OnCompleted/UnsafeOnCompleted`)。它允许任何类型（不仅仅是 `Task`）通过实现这些方法来变得“awaitable”，从而可以使用 `await` 关键字来等待它们的完成。在日常编程中，我们通常直接使用 `async/await` 关键字，而让编译器处理 `TaskAwaiter` 的细节。