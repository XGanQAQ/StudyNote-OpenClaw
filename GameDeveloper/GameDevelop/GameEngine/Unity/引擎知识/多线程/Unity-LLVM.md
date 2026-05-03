- 全称 **Low Level Virtual Machine**，直译为“低级虚拟机”。
    
- 但它已经不仅仅是虚拟机，而是一个 **编译器框架/基础设施**。
    
- 功能：提供优化、生成机器码等能力。很多现代语言（如 Swift、Rust、Clang/Cl）都基于 LLVM。
    
- 在 Unity 中，Burst 就是借助 LLVM 来把 C# 转成高效的原生机器码。

## 原理

LLVM是苹果公司开发的一项编译技术。编译器分三步：frontEnd、Optimizer、BackEnd。

![](https://pic3.zhimg.com/v2-7f3cd3bea2776d1fb026fcf9e568b78a_1440w.jpg)

frontEnd（前端）检查源代码是否存在错误，源代码进行抽象语法树分析，生成中间IR语言。

Optimizer(优化) 对中间IR语言进行优化，消除冗余计算，内联、变量折叠等。

BackEnd(后端) 最终将IR中间语言生成目标机器所能执行的代码。

经典的GCC编译器就是这个策略。

这个策略好是好，但是随着发展，开发语言越来越多，每套语言都得写套自己的编译器。而且目标机器也不一样，优化策略也不一样，比如X86,PowerPC,Arm等。

![](https://pic2.zhimg.com/v2-10d15b9b2754606b619b467f490f5f35_1440w.jpg)

而LLVM提供了一套LLVM IR的中间语言。前端无论是什么语言，只要通过语法分析生成LLVM所规定的IR中间语言，LLVM的优化以及后端最后都可以生成目标平台的机器码。

![](https://pic2.zhimg.com/v2-10d15b9b2754606b619b467f490f5f35_1440w.jpg)

  

![](https://pic4.zhimg.com/v2-a1d29c0f140b43af2ded894eb25a847d_1440w.jpg)

  

而Burst就是LLVM将C#代码转换成LLVM IR（Intermediate Representation）中间代码，然后通过LLVM的优化和代码生成功能生成目标平台的Native机器码。这个过程中，Burst利用了LLVM中内置的向量化指令优化技术，将一些常规的循环和算法转换成SIMD指令集，以实现对代码的高效优化。

另外，Burst还支持多线程编译，它会将每个被[BurstCompile]修饰的方法都分配给不同的线程去处理，以实现更快的编译速度。 

[Unity-Burst](Unity-Burst.md)