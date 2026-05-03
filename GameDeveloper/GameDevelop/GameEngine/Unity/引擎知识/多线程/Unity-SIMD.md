- 全称 **Single Instruction, Multiple Data**（单指令，多数据）。
    
- 一种 CPU **并行计算指令集**：一条指令可以同时处理多个数据（例如 4 个浮点数相加）。
    
- 在图形学、物理计算、AI、大量数学运算中，SIMD 能极大提升性能。
    
- Burst 会自动把数学、向量运算翻译成 SIMD 指令（比如 Intel AVX、ARM NEON）。