---
tags:
  - "#CSharp"
---

C# 中 `async` 和 `await` 语法糖的**本质**是：

**编译器在幕后将您的异步方法转换为一个状态机（State Machine）类。**

这个状态机类负责管理异步操作的暂停、恢复、状态保存、结果传递和异常处理，使得原本需要手动编写的复杂回调和流程控制变得像同步代码一样直观。

让我展开解释一下这个本质：

1. **从线性代码到事件驱动 / 回调：**
    
    - 您编写的 `async` 方法看起来是线性的，一行接一行地执行。
    - 但实际上，当遇到 `await` 关键字时，代码的执行流会“暂停”在当前位置，将控制权返回给调用者，而不是阻塞线程。
    - 一旦 `await` 的异步操作（比如 `Task.Delay` 或网络请求）完成，它会**触发一个回调**（continuation），这个回调会通知状态机继续执行 `await` 之后的代码。
    - 所以，`async`/`await` 的本质是将您线性的异步代码拆分成多个部分，通过**事件或回调机制**将这些部分连接起来。
2. **状态机的作用：**
    
    - **保存执行上下文：** 状态机类会保存方法中所有局部变量、参数以及当前执行到的位置（即 `await` 发生在哪一行）。这样，当异步操作完成后，方法可以从正确的位置和正确的上下文继续执行。
    - **管理控制流：** 状态机内部通常包含一个 `switch` 语句（或类似的逻辑），根据当前的状态（即 `await` 的哪个点）来决定从哪里恢复执行。
    - **桥接 `Task` 和回调：** `await` 关键字实际上是与 `Task` 对象的 `GetAwaiter()` 方法交互。这个 `Awaiter` 对象负责检查 `Task` 的完成状态，并在 `Task` 完成时安排状态机的方法（通常是 `MoveNext()`）被调用。
    - **统一异常和结果处理：** `Task` 内部的异常会被 `Awaiter` 捕获，并在恢复执行时重新抛出，以便您的 `try-catch` 块能够捕获。同样，`Task<TResult>` 的结果也会通过 `Awaiter` 提取并返回给您的代码。

**举个例子来比喻：**

想象您在看一本故事书。

- **同步代码**就像您从头到尾一页一页地读下去，直到读完。您在读书的时候不能做其他事情。
- **手动回调**（没有 `async`/`await`）就像您读到一半（比如“下回分解”），然后把书放下，写张纸条给您的朋友：“等这本书出下一集了告诉我，然后我就接着看。”当下一集出版后，您的朋友打电话通知您，您才拿起书接着看。这很麻烦，需要手动跟踪和通知。
- **`async`/`await` 就像您有一个智能管家。** 您告诉管家：“我开始看这本书。当遇到‘下回分解’时，你帮我盯着，下一集出了通知我，然后我接着看。”当您告诉管家后，您就可以去喝咖啡、做饭（主线程可以做其他事情）。当下一集出版后，管家会提醒您，然后您就从上次暂停的地方（状态机保存了您的阅读进度）拿起书继续看。这个“管家”就是编译器生成的**状态机**。

所以，`async`/`await` 的本质是 **将复杂的、基于回调的异步编程模型，通过编译器生成的智能状态机，转换成了看起来像同步、易于理解的线性代码。** 它抽象掉了底层线程管理、回调链、状态保存等复杂细节，让开发者能更专注于业务逻辑的实现。

### `async`/`await` 语法糖的“原本样子”

我们来看一个简单的 `async` 方法：

C#

```
// async/await 版本
public async Task<int> CalculateSumAsync(int a, int b)
{
    Console.WriteLine("CalculateSumAsync: 开始计算...");
    await Task.Delay(1000); // 模拟异步IO或耗时操作
    int sum = a + b;
    Console.WriteLine("CalculateSumAsync: 计算完成。");
    return sum;
}
```

在没有 `async`/`await` 的情况下，要实现类似的功能，我们需要手动：

1. **返回 `Task`：** 方法需要返回一个 `Task` 或 `Task<TResult>`。
2. **链式调用回调：** 使用 `ContinueWith` 方法来链式地连接异步操作完成后的回调。
3. **处理异常和取消：** 手动在回调中处理异常和取消。
4. **维护状态：** 如果有多个 `await`，需要在回调之间手动传递和保存局部变量的状态。

下面是 `CalculateSumAsync` 方法在没有 `async`/`await` 时的**大致**等效代码（这是一个简化的表示，实际编译器生成的代码会更复杂，包含更多的状态管理和异常处理逻辑）：

C#

```
// "原本的样子" (非常简化的手动实现，不完全等同于编译器生成的状态机)
public Task<int> CalculateSumManualAsync(int a, int b)
{
    // 创建一个 TaskCompletionSource 来管理 Task 的完成和结果
    TaskCompletionSource<int> tcs = new TaskCompletionSource<int>();

    Console.WriteLine("CalculateSumManualAsync: 开始计算 (第一部分)...");

    // 模拟 await Task.Delay(1000);
    Task.Delay(1000).ContinueWith(delayTask => // delayTask 是 Task.Delay 返回的 Task
    {
        // 检查上一个任务是否出错或被取消
        if (delayTask.IsFaulted)
        {
            tcs.SetException(delayTask.Exception.InnerException); // 将异常传递给 tcs
            return;
        }
        if (delayTask.IsCanceled)
        {
            tcs.SetCanceled(); // 设置 Task 为已取消
            return;
        }

        // 模拟 await 后的代码继续执行
        Console.WriteLine("CalculateSumManualAsync: 延时完成，继续计算第二部分。");

        int sum = a + b;
        Console.WriteLine("CalculateSumManualAsync: 计算完成。");

        // 设置 Task 的结果
        tcs.SetResult(sum);

    }, TaskScheduler.Default); // 确保在合适的调度器上执行回调

    return tcs.Task; // 立即返回未完成的 Task
}
```

### 编译器生成的实际状态机的工作原理（概念性描述）

当编译器处理 `async` 方法时，它会：

1. **重写方法签名：** 将 `async Task` 或 `async Task<TResult>` 方法转换为返回 `void`（对于异步 `Main` 方法或 `async void` 事件处理程序）或 `Task` / `Task<TResult>` 的普通方法。
2. **创建状态机类：** 为每个 `async` 方法生成一个内部的结构体或类。这个类会包含：
    - 一个 `int` 类型的字段来表示当前的状态（例如，0 表示初始状态，1 表示在第一个 `await` 之后，2 表示在第二个 `await` 之后等）。
    - 用于保存方法参数和局部变量的字段。
    - 一个 `IAsyncStateMachine` 接口的实现，包含 `MoveNext()` 方法和 `SetStateMachine()` 方法。
3. **`MoveNext()` 方法：** 这是状态机的核心。原始 `async` 方法的代码会被分解成多个块，每个 `await` 表达式都会将代码分解。`MoveNext()` 方法中包含一个 `switch` 语句，根据当前的状态（即 `await` 所在的行）来执行相应的代码块。
4. **在 `await` 处：** 当 `MoveNext()` 执行到 `await` 表达式时：
    - 它会捕获 `await` 表达式之后的代码作为回调。
    - 它会将当前状态保存到状态机字段中。
    - 它会调用 `TaskAwaiter` （由 `await` 运算符生成）来检查 `Task` 是否已完成。
    - 如果 `Task` 未完成，`TaskAwaiter` 会安排一个延续（continuation），当 `Task` 完成时，这个延续会再次调用状态机的 `MoveNext()` 方法。
    - 然后 `MoveNext()` 方法会立即返回，将控制权交还给调用方，从而实现非阻塞。
5. **`Task` 完成后：** 当 `await` 的 `Task` 完成时，之前安排的延续会被执行，它会调用状态机的 `MoveNext()` 方法。`MoveNext()` 会根据保存的状态从上次离开的地方继续执行。
6. **结果和异常：** `TaskAwaiter` 负责从完成的 `Task` 中提取结果或捕获异常，并将其传递给状态机。异常会在 `MoveNext()` 中被重新抛出，以便被 `try-catch` 块捕获。

### 总结 `async`/`await` 是语法糖的好处：

- **极大地简化代码：** 将复杂的异步模式（回调、状态管理、异常传递）隐藏在简单的 `await` 关键字之后。
- **提高可读性：** 异步代码看起来像同步代码，更容易理解和维护。
- **减少错误：** 编译器处理了大量的复杂性，减少了手动编写异步逻辑时引入 bug 的可能性。
- **类型安全：** `await` 能够直接返回 `Task<TResult>` 的结果，而不是通过回调参数传递。

所以，当你说 `async`/`await` 是 `Task` 的语法糖时，你非常正确。它将手动编写 `Task.ContinueWith`、`TaskCompletionSource` 以及状态管理的代码，变成了编译器自动为您生成的强大机制。