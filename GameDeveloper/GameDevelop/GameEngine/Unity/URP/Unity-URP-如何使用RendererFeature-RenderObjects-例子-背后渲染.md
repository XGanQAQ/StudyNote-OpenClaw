## 参考教程
[Unity - Manual: Example of creating a custom rendering effect using a Render Objects Renderer Feature in URP](https://docs.unity3d.com/6000.1/Documentation/Manual/urp/renderer-features/how-to-custom-effect-render-objects.html)

## 实现原理
在URP Renderer Asset中关闭掉渲染此层级的物体，并利用2个RenderFeature的Render Objects对其进行渲染
- RenderObjectsBehind
	- 当此像素的深度缓冲区中有大于 准备要渲染的像素的时候，渲染上此像素
- RenderObjectsFront
	- 替代掉原本渲染不被遮挡的时候的在原管线的渲染，就是正常渲染的部分
本质上是通过改变物体的渲染顺序
## 详细步骤

**设置Layer**
为一个对象分配一个Layer 名为 **DrawBehind**

**设置RendererData**
![](Pasted%20image%2020260221071310.png)
将设置的Layer从OpaqueLayerMask中剔除
这样Layer中的物体就不会被渲染，让其通过RendererFeature进行渲染

**设置RendererFeature**
找到你对应的 URP Renderer asset
然后点击 Add Renderer Feature 选择添加一个 Render Objects.
将Layer Mask 设置为你之前分配的Layer，并将 Event 设置为 AfterRenderingOpaques

打开 Overrides 选择 Depth 设置 Depth Test 为 Greater.
创建一个材质，设置上你想要的颜色，并将overrides中的材质设为它

新添加一个RenderObjects
Layer Mask选择此物体层级，Event为 AfterRenderingOpaques
关闭深度写入

![](Pasted%20image%2020260221071526.png)


![](Pasted%20image%2020260221070857.png)

>  [Unity-URP-官方默认RendererFeature介绍-如何编写自定义RendererFeature](Unity-URP-官方默认RendererFeature介绍-如何编写自定义RendererFeature.md)


