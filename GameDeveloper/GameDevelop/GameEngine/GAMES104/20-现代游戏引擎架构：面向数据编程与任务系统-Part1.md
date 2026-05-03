## 并行计算基础 Basics of Parallel Programing

Process and thread 进程和线程

Types of Multitasking
- 抢占式多重任务处理
	- 可被调度器中断
	- 调度器决定哪一个任务应该被执行
	- 大多数操作系统的使用
- 非抢占式
	- 任务必须清晰的规划好让步控制
	- 必须和调度方案协作工作
	- 许多高要求的实时操作系统会使用这种方案

Thread Context Switch 线程内容切换
- 切换开销
- 缓存开销
线程之间的切换很贵

Parallel Problems in Parallel Computing
平行问题平行计算

Data Race 数据竞争

Blocking Algorithm - Locking Primitives 锁

锁的问题
- 死锁
- task不一定完成

原子性操作

Wait Free 等待为0编程

执行顺序-编译优化
高级语言写的代码执行的过程不一定按照你所设想的顺序运行

## Parallel Framewrok of Game Engine

Fixed Multi-thread 固定多线程
按功能模块分配到对应的线程
- 有的线程工作量大有的小

Thread Fork-Join
到一定时期，固定好的线程 Fork出子线程，最后再合并

Unreal Parallel framewrok
- Named Thread
- Worker Thread

### Task Graph

根据任务之间的依赖，构建好任务图，让CPU自动分析依赖并行执行
问题是 实际游戏开发会不断有动态的依赖任务

## Job System

### Coroutine
协程 轻量多线程的方法
执行权让步、用户态线程

Coroutine vs Thread
线程切换成本高
协程之间的切换成本低

Coroutine协程的类型
- Stackful Conroutine
	- 切换栈，而不是重写代码
- Stackless Coroutine
	- 把函数改写成一个状态机类
区别
真正的分类其实是三层：
1. OS Thread（操作系统线程）
2. Stackful User Thread（用户态线程）
3. Stackless Coroutine（状态机）

性能从低到高：  
线程 < stackful < stackless

表达能力从强到弱：  
线程 > stackful > stackless

**Stackful 协程通过“切换独立栈”保存完整调用链。**  
**Stackless 协程通过“编译器生成状态机”保存函数执行进度。**  
**C# async 和 Unity Coroutine 都属于 Stackless。**


Couroutine在普通平台的支持不同

### Fiber-based Job System

让任务“主动让出执行权”，而不是阻塞线程。

Fiber（协程/轻量线程）是一种：
> 用户态线程（User-space thread）
> Fiber = 一种 stackful coroutine

LIFO and FIFO Mode
- First In First Out
- Last In First Out

Pros and Cons of Job System


## 疑问
- 协程任然是在一个线程上工作，那么为什么使用协程可以让程序更流畅的运行呢？
	- 把一个长时间任务  拆分为多个短时间片  插入到主循环之间
- 协程是如何控制应该什么时候让出控制器的，以Unity的实现为例
	- 协程“让出控制权”的时机就是：当执行到 `yield return` 那一行时立即让出











