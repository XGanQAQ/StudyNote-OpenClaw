
[Unity - Manual: Injection points reference for URP](https://docs.unity3d.com/6000.1/Documentation/Manual/urp/customize/custom-pass-injection-points.html)关于对于Renderer Feature 渲染pass注入点的文档

## 🧩 一、Unity URP 官方内置的 Renderer Feature 介绍

在 **Universal Render Pipeline (URP)** 中，**Renderer Feature** 是一种可插拔的渲染扩展机制，用来在渲染流程中插入自定义的 Pass。

Unity 官方在 URP 中内置了几种常见的 Renderer Feature，它们都在 “Universal Renderer Data” 资源中可见（例如 `ForwardRenderer.asset`）。

以下是常见的官方 Renderer Feature：

|名称|主要作用|对应 Pass|常见用途|
|---|---|---|---|
|**Render Objects**|自定义绘制特定对象（基于 Layer 或 Tag），并可设置自定义 Shader、渲染队列、Blend 模式等。|`RenderObjectsPass`|例如：绘制轮廓线、绘制特定层的物体、绘制阴影掩码|
|**Screen Space Shadows**|生成屏幕空间阴影纹理，用于优化阴影显示。|`ScreenSpaceShadowsPass`|优化阴影性能（仅在支持的设备上）|
|**Screen Space Ambient Occlusion (SSAO)**|实时计算屏幕空间环境光遮蔽。|`ScreenSpaceAmbientOcclusionPass`|添加细节阴影效果，提升深度感|
|**Bloom**|屏幕后期发光效果。|`BloomPass`|提升画面亮度与氛围|
|**DepthNormalsTexture**|生成深度+法线贴图，供其他特效（如SSR、SSAO）使用。|`DepthNormalsPass`|为后期特效提供输入|
|**Render Graph Debug Passes**|用于调试 Render Graph 输出。|—|开发调试使用（Unity 2023+）|

> 🧠 小结：
> 
> - **Render Objects** → 自定义物体绘制
>     
> - **SSAO/Bloom** → 后处理
>     
> - **DepthNormals** → 提供深度法线信息
>     
> - **ScreenSpaceShadows** → 阴影优化
>     

---

## 🧠 二、Renderer Feature 的运行机制

URP 渲染过程是一个有序的 **Render Pass Pipeline**，Renderer Feature 允许你：

1. 在渲染流程中插入自己的 **Pass**（如 Before Rendering / After Rendering）。
    
2. 控制何时、如何、绘制什么。
    

机制如下图所示：

```
Camera Render
 ├─ Setup
 ├─ Depth Prepass
 ├─ Opaque Pass
 ├─ Skybox
 ├─ Transparent Pass
 ├─ Post Processing
 └─ Custom Passes (Your Feature)
```

Renderer Feature 是一个 ScriptableObject：

- 它在 **初始化时创建 Pass 实例**；
    
- 在渲染时将 Pass **注入到管线的特定阶段**；
    
- 每个 Pass 继承自 `ScriptableRenderPass`。
    

---

## 🧱 三、如何编写自定义 Renderer Feature（完整模板）

下面是一个官方推荐的模板结构（适用于 Unity 2022+ URP）：

### 📄 1. 自定义 Renderer Feature 脚本

```csharp
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class CustomRenderFeature : ScriptableRendererFeature
{
    class CustomRenderPass : ScriptableRenderPass
    {
        private string profilerTag = "Custom Render Pass";
        private Material material;
        private RenderTargetIdentifier source;
        private RenderTargetHandle tempTexture;

        public CustomRenderPass(Material material)
        {
            this.material = material;
            tempTexture.Init("_TempTex");
        }

        public void SetSource(RenderTargetIdentifier src)
        {
            source = src;
        }

        public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
        {
            if (material == null) return;

            CommandBuffer cmd = CommandBufferPool.Get(profilerTag);

            // 获取渲染目标尺寸
            RenderTextureDescriptor descriptor = renderingData.cameraData.cameraTargetDescriptor;
            descriptor.depthBufferBits = 0;

            // 创建临时RT
            cmd.GetTemporaryRT(tempTexture.id, descriptor, FilterMode.Bilinear);

            // 执行Blit（相当于Graphics.Blit）
            Blit(cmd, source, tempTexture.Identifier(), material);
            Blit(cmd, tempTexture.Identifier(), source);

            context.ExecuteCommandBuffer(cmd);
            CommandBufferPool.Release(cmd);
        }

        public override void FrameCleanup(CommandBuffer cmd)
        {
            if (cmd == null) return;
            cmd.ReleaseTemporaryRT(tempTexture.id);
        }
    }

    [System.Serializable]
    public class Settings
    {
        public Material material = null;
        public RenderPassEvent renderPassEvent = RenderPassEvent.AfterRenderingTransparents;
    }

    public Settings settings = new Settings();

    CustomRenderPass customPass;

    public override void Create()
    {
        customPass = new CustomRenderPass(settings.material)
        {
            renderPassEvent = settings.renderPassEvent
        };
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        customPass.SetSource(renderer.cameraColorTargetHandle);
        renderer.EnqueuePass(customPass);
    }
}
```

### 📌 2. 使用方法

1. 创建一个 `Material`，指定你自己的 Shader（如后处理特效）。
    
2. 在 **Forward Renderer Data** 中添加 “CustomRenderFeature”。
    
3. 将该 Material 拖入 Feature 的 `material` 字段。
    
4. 设置 `RenderPassEvent`（如 AfterRenderingPostProcessing）。
    

---

## 💡 常见 RenderPassEvent 注入点

|事件|时机|说明|
|---|---|---|
|`BeforeRendering`|渲染前|自定义预处理，例如深度|
|`BeforeRenderingSkybox`|天空盒前|适合画背景层|
|`AfterRenderingOpaques`|不透明物体后|常用于轮廓、描边|
|`AfterRenderingTransparents`|透明物体后|常用于后期特效|
|`AfterRenderingPostProcessing`|后处理后|叠加特效|
|`AfterRendering`|全部渲染完后|通常用于调试输出|

---

## 🧠 四、推荐学习方向

|目标|建议学习内容|
|---|---|
|想做描边效果|了解 `RenderObjectsFeature` 的实现方式|
|想做后处理滤镜|学习 `CustomRenderFeature + Blit` 模式|
|想优化性能|学习 `RenderGraph` 和 `DepthNormalPass`|
|想完全掌握渲染管线|阅读 `UniversalRenderPipeline.cs` 源码|
