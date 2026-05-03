非图形应用使用GPU的情况，我们称之为**GPGPU**（General Purpose GPU）编程

涉及到将数据从GPU显存（Video Memory）中拷贝到CPU系统内存（System Memory）中的操作，该操作非常的**慢**。但是相比使用GPU来计算所提升的运行速度而言，可以忽略此问题。

瓶颈在于CPU和GPU之间的内存传输。

要实现GPGPU编程，我们需要一个方法来访问GPU从而实现数据并行算法

Compute Shader（后面简称为CS）。CS属于图形API中的一种可编程着色器，它独立于渲染管线之外

由于CS可以直接读写GPU资源，使得我们能够将CS的输出直接绑定到渲染管线上。因此对于图形应用，我们通常使用GPU的计算结果作为渲染管道的输入，因此不需要将结果从GPU传输到CPU。

例如我们要实现一个模糊效果，可以先用CS模糊一个Texture，然后模糊后的Texture可以直接作为Fragment Shader的输入。
## 参考

- [【Unity】Compute Shader的基础介绍与使用 - 知乎](https://zhuanlan.zhihu.com/p/368307575)
- [Unity - Manual: Introduction to compute shaders](https://docs.unity3d.com/Manual/class-ComputeShader-introduction.html)