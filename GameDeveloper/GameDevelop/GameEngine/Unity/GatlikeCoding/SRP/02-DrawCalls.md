## Shaders

### Unlit Shader

### 1.2 HLSL Programs

### 1.3 Include Guard

Include 保护，保证相同内容不被重复编译
```cs
#ifndef CUSTOM_UNLIT_PASS_INCLUDED
#define CUSTOM_UNLIT_PASS_INCLUDED
#endif
```

### 1.4 Shader Functions

教程中把include放在后面，我实际的操作发现会报错丢失符号链接。把include放在上面即可。

in the .hlsl to comple the vertex/fragment function

hlsl中 很一个很关键的部分——语义 semantics 。 我们需要用他给函数/参数做标记

```cs
float4 UnlitPassFragment () : SV_TARGET {
	return 0.0;
}
```

### 1.5 Space Transformation 空间变换

想要让顶点正确的渲染到屏幕上，需要通过空间变换。空间变换需要使用空间变换相关的变换矩阵

为了统一和方便Shader编写过程中，对于顶点空间变换的操作，我们创建了一个ShaderLibrary的文件夹，并存放相关的hlsl文件，写上常见的通用的空间变换函数，并将其在shader中调用。

>[!Tips] Unity 是如何自动将它在内部维护的对应矩阵值传递给你的着色器的？
>Unity 有一套预定义的**内置着色器变量 (Built-in Shader Variables)**。这些变量的命名是固定的，当你以特定的名称（比如 `unity_ObjectToWorld`、`unity_MatrixVP` 等）在 HLSL 着色器中声明它们时，Unity 渲染管线会自动识别它们。

### 1.6 Core Library

我们通过引入 Core RP Pipeline 的包，来替换Comman.hlsl的变换函数，而不是自己去写。

### 1.7 Color

给shader的properties块添加属性，让其可以在编辑器中修改

## 2. Batching 批处理

每个Draw call 都需要CPU和GPU之间进行通信，
如果需要向GPU发送大量数据
- GPU需要等待数据，浪费时间
- CPU需要忙于发生数据
这俩者都会导致帧率下降

### 2.1 SRP Batcher

**原理：** SRP 批处理并非减少绘制调用的数量，而是使其更精简。它将材质属性缓存在 GPU 上，这样就不必在每次绘制调用时都发送它们。这既减少了需要通信的数据量，也减少了 CPU 每次绘制调用需要完成的工作。但这只有在着色器遵循严格的统一数据结构时才有效。

根据教程，我在frame debugger 中 看到绘制调用SRP Batch
SRP Batch 不是只有一个draw call 而是经过优化的绘制调用序列

>[!question] 使用SRP Batcher 为什么 Batch 的数量没有变化？
>**SRP Batcher** 的主要目标是减少 **CPU 端的 SetPass Calls**。它通过将相同 Shader 但不同材质的物体数据打包到 GPU 的一个大缓冲区中，让 GPU 循环处理，从而避免 CPU 频繁地重新设置渲染状态。因此，**CPU 的渲染时间 (CPU Rendering time)** 会显著降低，而不是 `Draw Calls` 数量。

### 2.2 Many Colors

多个材质使用同一个Shader，SRP Batcher 依旧可以工作，让其只有一个批次。
但是如果想要给多个物体设置不同的材质颜色，就需要给每个物体设置一个单独的材质，这样太麻烦了。

我们可以通过自定义组件的方式，用c#组件，来获得Shader并创建材质属性面板，赋值给Render
```cs
[DisallowMultipleComponent]  
public class PerObjectMaterialProperties : MonoBehaviour {  
    static int baseColorId = Shader.PropertyToID("_BaseColor");  
    static MaterialPropertyBlock block;  
        [SerializeField]  
    Color baseColor = Color.white;  
    void Awake () {  
        OnValidate();  
    }    void OnValidate () {  
        if (block == null) {  
           block = new MaterialPropertyBlock();  
        }        block.SetColor(baseColorId, baseColor);  
        GetComponent<Renderer>().SetPropertyBlock(block);  
    }}

```

### 2.3 GPU Instancing

**原理：** GPU 实例化，其工作原理是同时对具有相同网格的多个对象发出单个绘制调用。CPU 收集所有每个对象的变换和材质属性，并将它们放入数组中发送给 GPU。然后，GPU 会迭代所有条目，并按照提供的顺序进行渲染。

GPU 实例化仅适用于共享相同材质的对象。

想要让材质能使用 GPU Instancing 需要对Shader进行修改，使用GPU Instancing 相关宏。

### 2.4 Drawing Many Instanced Meshes

我们可以利用 GPU Instancing 绘制大量的对象

我们写了一个脚本绘制大量网格

### 2.5 Dynamic Batching

动态批处理。这是一种古老的技术，它将多个共享相同材质的小网格合并成一个更大的网格，然后再进行绘制。

总体而言，GPU 实例化比动态批处理效果更好。

### 2.6 Configuring Batching

通过变量，来将上述处理设置为可配置。

最终在 CustomRenderPipelineAsset 创建的 Asset 的中配置

## 3 Transparency

修改我们的Unlit Shader 让其同时支持 不透明 和 透明 渲染

### 3.1 Blend Modes

不透明渲染和透明渲染之间的主要区别在于，我们是否替换之前绘制的内容，还是将其与之前的结果相结合以产生透视效果。

> Here source refers to what gets drawn now and destination to what was drawn earlier and where the result will end up.

Src Blend 就是决定怎么处理自身的绘制
Dst Blend 处理怎么混合绘制到目标区域

### 3.2 Not Writing Depth

透明渲染通常不会写入深度缓冲区，因为它不会从中受益，甚至可能产生不理想的结果。我们可以通过 `ZWrite` 语句控制是否写入深度。

### 3.3 Texturing 

纹理必须要上传到 GPU 内存，Unity 会帮我们完成这项工作。
我们使用 `TEXTURE2D` 宏 （指向纹理的句柄）和  `SAMPLER` 宏 （进行采样）

并添加纹理相关变量，并在顶点着色器中传递采样器，在片元着色器中调用采样器采样

### 3.4 Alpha Clipping Alpha

Alpha clipping 透明度裁剪
通常的做法是定义一个截止阈值。Alpha 值低于此阈值的片段将被丢弃，而其他所有片段将被保留。

材质通常使用透明度混合或 Alpha 裁剪，而不是同时使用两者。

典型的裁剪材质除了丢弃的片段外完全不透明，并且会写入深度缓冲区。它使用 `AlphaTest` 渲染队列，这意味着它会在所有完全不透明的对象之后渲染。

我们还可以使用一个`Toggle` 特性来控制着色器关键字，对Alpha clipping 进行开关

### 3.5 Shader Features

我们通过 Toggle 和 Shader_feature 来生成Shader的变体

### 3.6 Cutoff Per Object 每个对象的裁除

我们为之前写的per object控制器添加对于透明度裁剪的控制

### 3.6 Ball of Alpha-Clipped Spheres

修改随机生成细节