
[Data-Oriented_Technology_Stack_for_advanced_Unity_users_2022_LTS_final](Data-Oriented_Technology_Stack_for_advanced_Unity_users_2022_LTS_final.pdf)

## Best Start

[Unity-Technologies/EntityComponentSystemSamples](https://github.com/Unity-Technologies/EntityComponentSystemSamples/tree/master)

## CSharp Job System

included in the Unity core module

Unity的主要逻辑都跑在CPU主线程上。如果手动创建管理额外的线程，是非常不安全且低效且困难的
所以Unity提供了C# Job System

- Job System 维护着一个对象池，针对不同的平台创建不同数量的Work threads
- Worker thread 会执行名为 jobs 的任务。在work thread idel的时候，他会拉取下一个可获取的job去执行（从queue中）
- 一旦job开始执行 在worker thread 上，直到运行完成

### 调度安排Job

- Jobs只能从main thread被安排，不能从别的Jobs
- 在主线程 调用一个已经被安排的 `Complete()` 方法时，他会等待job执行完成
- 只有主线程可以调用`Complete()`
- 在调用 `Complete()` 函数后，您可以确定该任务所使用的数据在主线程中再次可以安全访问，并且可以安全地传递给后续调度的任务。

### Job 安全检查和依赖

为了保证安全和线程之间的依赖管理，多线程编程中很重要的是防止竞争情况，数据占用和其他同步问题。
接下来介绍Job System是如何解决这些安全和依赖问题的

- 为了确保隔离性，每个job都有自己私有的数据，其他线程/jobs无法访问
- 然而jobs之间或者jobs和主线程可能存在数据共享。有着共享相同数据的情况，俩者不能同时运行。
- 在你调度job的时候，你可以声明他依赖的job。在它依赖的job执行完后，它才会开始执行
- 一个job在执行完后，其依赖的job直接/间接的执行完成

如果有涉及到数据IO/网络调用的部分，请使用异步 APIs。
因为这部分的读取会造成长时间的卡顿。

## The Brust compiler 编译器

起初，CSharp 代码默认使用Mono编译（ 是一个即时编译器 JIT）
后来可以使用 IL2CPP （提前编译器 AOT）可以提供更好的运行时性能，且可以更好的支持一些特定的平台

Brust Package 提供了第三个编译器，进行了更深度的优化，其运行性能会比 Mono甚至IL2CPP更好。

但是 Brust 只能编译部分C#代码

> The main limitation is that Burst-compiled code can’t access managed objects, including all class instances

>**由 .NET / C# 运行时（CLR）管理生命周期的对象**，它们通常分配在 **托管堆（Managed Heap）** 上，由 **垃圾回收（GC）** 自动管理。
>只要是 `class` 创建出来的对象，基本都是 managed object。

## Collections 集合

> The Collections package provides unmanaged collection types, such as lists and hash maps

 Collections package 提供一些不受管理的集合类型

不受管理 指的是 不被 C#运行时管理，不被垃圾回收管理

不被垃圾回收管理，则可以更安全的在jobs和Brust中使用

Collection Types 有如下策略

- 类型以 **Native** 开头。出现如下情况会抛出异常
	- 没有进行合适的 disposed
	- 线程不安全的在Jobs被使用
- 名称以“Unsafe”开头的类型不进行任何安全性检查。
- 其余那些既不属于“原生”类型也不属于“不安全”类型的类型是不含指针的小型Struct结构体类型，因此它们根本不会被分配内存。因此，它们无需进行释放操作，也不存在潜在的线程安全问题。 

一些原生类型都有其对应的非安全版本。例如，既有原生列表（NativeList）又有非安全列表（UnsafeList），还有原生哈希表（NativeHashMap）和非安全哈希表（UnsafeHashMap）等成对的实例。出于安全考虑，在可能的情况下，您应优先使用原生集合而非其对应的非安全版本。

## Mathematics 数学

Mathematics 包 是一个 C# 数学库，就像Collections.
它提供了一下比C#/IL 更高效的Native Code

- 向量矩阵类型
- Many math methods and operators that follow HLSL-like shader conventions
- Special Burst compiler optimization hooks for many methods and operators

许多 UnityEngine.Mathf库的方法和类型无法在Brust Compiled Code中运行。但是Unity.Mathematics会在某些情况下运行的更好

## Entities (ECS) 实体

Entities Package 提供了ECS的一种实现。
ECS是一个编程范式 由 entities 实体、component组件、systems系统 组成进行编程

Entities 由 Component组件组成，这些组件一般是C# Struct结构体。
就像GameObject，一个entities的组件在生命周期期间被添加和删除

不像GameObjects
**待续**

### Archetypes 原型

包含一组有着相同组件的Entities

### Chunks

> Within an archetype, the entities and their components are stored in blocks of memory called chunks



