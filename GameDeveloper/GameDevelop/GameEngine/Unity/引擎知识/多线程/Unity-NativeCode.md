- 指 **CPU 可以直接执行的二进制指令**（汇编级别）。
    
- 相对的，C# 默认运行在 **.NET/Mono 虚拟机（IL，Intermediate Language）** 上，需要解释或 JIT 才能执行，性能较差。
    
- Burst 可以跳过中间层，直接生成 **CPU 本地指令**，所以快。

[Unity-Burst](Unity-Burst.md)