【【Unity教程-Shadergraph】故障效果】 https://www.bilibili.com/video/BV1pw4m1e7Ty/?share_source=copy_web&vd_source=445f9fe806d1b40f2620f76957091c99

- 将贴图的RGB三色分开处理然后再合并
- 将UI 加减一个参数分别分配给3个RGB进行UV偏移
- 使用噪声对

Unity的Shader Graph的posterize的节点是什么作用
将连续的色彩或数值梯度**量化**成数量更少的、离散的色块或数值等级
它将输入值（例如颜色、UV坐标等）限制在一个预设的**步数 (Steps)** 内。

**工作原理（数学表达式示例）**：

虽然具体的实现可能有所不同，但核心思路通常是：

$$\text{Out} = \text{floor}(\text{In} \times \text{Steps}) / \text{Steps}$$

其中：
- $\text{In}$ 是输入值 (例如 0 到 1 之间的颜色分量)。
- $\text{Steps}$ 是步数（你想要分成的等级数量）。
- $\text{floor}(\dots)$ 是向下取整操作。

这个公式将输入值 $\text{In}$ 映射到 $\text{Steps}$ 个离散的等级之一。