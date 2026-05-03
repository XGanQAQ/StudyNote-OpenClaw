
>Although this already appears to work, the result is currently incorrect. What appears higher should appear lower instead, and vice versa. This happens because the vectors from the normal map exist in texture space and have to be converted to world space to affect lighting. This requires a transformation matrix, which defines a 3D space relative to the surface, known as tangent space. It consists of a right, an up, and a forward axis.

- **法线贴图存储的法线向量是“局部”的**，它们是在一种名为“切线空间”的坐标系中定义的，这个切线空间是相对于模型表面的。
- 为了让这些法线向量参与到全局的光照计算中（因为光照是在世界空间中进行的），它们必须**从切线空间转换到世界空间**。
- 这个转换需要一个**变换矩阵**。这个矩阵由切线空间的三根轴（切线、副切线、法线）构成，这些轴在世界空间中定义了模型表面上每一点的局部方向。