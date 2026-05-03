## 参考资料
- [Unity JobSystem使用及技巧 - 飞翔的子明 - 博客园](https://www.cnblogs.com/FlyingZiming/p/17241013.html)
- [20.现代游戏引擎架构：面向数据编程与任务系统 (Part 1) | GAMES104-现代游戏引擎：从入门到实践_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1EP411V7jx/?vd_source=1015af2504b4c9c5deda584505666669)

## 🔹 Job System 是什么？

**Unity Job System** 是 Unity 引入的一套 **多线程任务调度框架**，帮助开发者更方便地利用多核 CPU 来并行执行代码，从而提升性能。

它的目标是：

- 简单（开发者不需要手写复杂的多线程同步代码）。
    
- 安全（避免数据竞争，保证线程安全）。
    
- 高效（充分利用 CPU 多核并行）。
    

---

## 🔹 为什么需要 Job System？

- 默认的 Unity 逻辑大多在 **主线程** 上执行（比如 `Update()`）。
    
- 如果逻辑计算量大（AI、物理计算、数据处理等），就会 **卡帧**。
    
- 多核 CPU 本来可以同时干活，但手写多线程很麻烦，还容易出错（死锁、竞争条件）。
    
- Job System 提供了一个 **声明式的 API**，让你写的代码可以自动并行化，并且由 Unity 负责调度和同步。
    

---

## 🔹 工作原理

Job System 的核心就是：**把计算任务（Job）分配到多个 CPU 线程执行**。

大致流程：

1. 你定义一个 **Job**（需要执行的任务）。
    
    - Job 是一个实现 `IJob`、`IJobParallelFor` 等接口的结构体。
        
2. 调用 `Schedule()` 把这个 Job 提交给 Unity Job System。
    
3. Unity 的 **Job Scheduler（调度器）** 会把 Job 分配到工作线程池中执行。
    
4. 你可以选择等待结果（`jobHandle.Complete()`），或者让它在后台完成。
    

---

## 🔹 Job System 的常用接口

1. **IJob**
    
    - 定义一个单一任务。
        
    
    ```csharp
    public struct MyJob : IJob
    {
        public void Execute()
        {
            // 这里写任务逻辑
        }
    }
    ```
    
2. **IJobParallelFor**
    
    - 定义一组可以并行运行的任务，类似 `for` 循环并行化。
        
    
    ```csharp
    public struct MyParallelJob : IJobParallelFor
    {
        public NativeArray<float> data;
        
        public void Execute(int index)
        {
            data[index] = math.sqrt(data[index]);
        }
    }
    ```
    
3. **JobHandle**
    
    - 表示一个 Job 的“句柄”，用来：
        
        - 控制依赖关系（让某个 Job 等另一个 Job 执行完再跑）。
            
        - 等待完成（`jobHandle.Complete()`）。
            

---

## 🔹 与 Burst 的关系

- **Job System** 提供了 **任务并行化的调度机制**。
    
- **Burst Compiler** 把 Job 中的 C# 代码编译为高效的本机 SIMD 代码。
    
- 二者结合：既能充分利用 **多核 CPU**，又能充分利用 **单核指令优化**。
    

---

## 🔹 举个例子

比如：你要计算 100 万个数的平方根。

- **传统做法**：在 `Update()` 里用 for 循环，全部在主线程执行 → 卡顿。
    
- **Job System**：用 `IJobParallelFor`，把计算分成多份，丢给 CPU 多核并行 → 快很多。
    
- **加上 Burst**：编译成 SIMD 指令 → 再快一倍以上。
    

---

## 🔹 总结

- **Job System** = 多线程任务框架（并行化）。
    
- **Burst** = 高性能编译器（指令级优化）。[Unity-Burst](Unity-Burst.md)
    
- **ECS（Entity Component System）** = 数据布局优化（Cache Friendly）。
    

三者结合就是 Unity 的 **DOTS（Data-Oriented Technology Stack）**，主打高性能。