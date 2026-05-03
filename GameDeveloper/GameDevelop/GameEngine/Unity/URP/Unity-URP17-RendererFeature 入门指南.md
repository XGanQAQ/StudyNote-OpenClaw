
## 参考资源
- [Unity6-URP17Renderer Feature 入门指南]( https://www.bilibili.com/video/BV1BzzJYxERU/?share_source=copy_web&vd_source=445f9fe806d1b40f2620f76957091c99)
- 项目仓库: https://github.com/wenhaoGit/URP_17_RenderFeature
- 场景素材: https://assetstore.unity.com/packages/essentials/starter-assets-thirdperson-updates-in-new-charactercontroller-pa-196526
## 基础

基础使用例子
1. 更改渲染对象的属性
2. 更改渲染的顺序
3. 利用相机缓冲区的数据在Shader中使用

配置文件
![](Pasted%20image%2020260221070353.png)
- RenderPiplineAsset
	- ![](Pasted%20image%2020260221070206.png)
	- ProjectSetting-> Quality -> RenderPiplineAsset
	- 一个项目只有一个正在被启用
- Renderer Data
	- 一个项目中会有多个RendererData, 
	- 需要存放到RenderPiplineAsset的RendererList之下启用
		- ![](Pasted%20image%2020260221070118.png)
	- 相机可以选择不同的RendererData(已放RendererList)
		- ![](Pasted%20image%2020260221070328.png)
- ScriptableRendererFeature

内置RendererFeature
- Screen Space Ambient Occlusion
	- 基于屏幕空间的环境光遮蔽
- FullScreenPassRendererFeature
	- 自定义屏幕空间处理
	- [Unity-Shader-FullScrennShaderGraph](Unity-Shader-FullScrennShaderGraph.md)
	- 屏幕雾效
- RenderObjects
	- 自定义物体渲染处理
	- [Unity-URP-如何使用RendererFeature-RenderObjects-例子-背后渲染](Unity-URP-如何使用RendererFeature-RenderObjects-例子-背后渲染.md)
	- 遮挡显示
- ScreenSpaceShadow
	- 屏幕空间的阴影映射（替代默认的方案）
	- URP默认使用的是级联阴影
		- 根据不同的距离，渲染不同精度的阴影
- Decal
	- 贴花系统（DecalProjector）依赖项

### FullScreenPassRendererFeature-简单雾效

利用 FullScreenShaderGrpah + FullScreenPassRendererFeature 实现简单的雾效

![](Pasted%20image%2020260221082319.png)
![](Pasted%20image%2020260221082250.png)

## 进阶

![](Pasted%20image%2020260221084620.png)
**RenderPass 具体的渲染流程**

**RenderGraph 渲染相关的资源管理**
![](Pasted%20image%2020260221085246.png)

**RenderGraph Viewer**
可以直观的观察到，各种Render资源的写入和读取
![](Pasted%20image%2020260221085841.png)
- 红色 写入
- 绿色 读取
- 灰色 已写入、目前未使用
一些Pass会自动合并

## 自定义实现

### 自定义RendererFeature 模板
```cs
﻿using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class CustomRendererFeature : ScriptableRendererFeature
{
    private CustomRenderPass renderPass;


    public override void Create()
    {
        renderPass = new CustomRenderPass();
        renderPass.Init();
    }

    public override void SetupRenderPasses(ScriptableRenderer renderer, in RenderingData renderingData)
    {
        renderPass.Setup();
    }

    protected override void Dispose(bool disposing)
    {
        renderPass.Dispose();
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        SetupRenderPasses(renderer, renderingData);
        renderer.EnqueuePass(renderPass);
    }
}
```

### 自定义RenderPass模板
```cs
﻿using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class CustomRenderPass : ScriptableRenderPass
{
    private class CustomPassData
    {

    }

    public void Init()
    {
        profilingSampler = new ProfilingSampler("CustomRenderPass");
        renderPassEvent = RenderPassEvent.BeforeRenderingOpaques;
    }

    public void Setup()
    {
    }

    public void Dispose()
    {
    }

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        base.RecordRenderGraph(renderGraph, frameData);

        using (var builder = renderGraph.AddRasterRenderPass<CustomPassData>(passName, out CustomPassData data))
        {
            //passdata
            //data.xx = 

            //read
            //builder.UseTexture  builder.UseRendererList

            //write
            //builder.SetRenderAttachment 

            //process
            builder.SetRenderFunc<CustomPassData>((CustomPassData data, RasterGraphContext context) => ExecutePass(data, context));
        }
    }

    private void ExecutePass(CustomPassData data, RasterGraphContext context)
    {
        //process
        //Blitter.blit  context.cmd.DrawMesh 
    }
}
```

### 自定义深度雾RendererFeature

```cs
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class ScreenDepthRendererFeature : ScriptableRendererFeature
{
    private ScreenDepthRenderPass renderPass;


    public override void Create()
    {
        renderPass = new ScreenDepthRenderPass();
        renderPass.Init();
    }

    public override void SetupRenderPasses(ScriptableRenderer renderer, in RenderingData renderingData)
    {
        renderPass.Setup();
    }

    protected override void Dispose(bool disposing)
    {
        renderPass.Dispose();
    }

    public override void AddRenderPasses(ScriptableRenderer renderer, ref RenderingData renderingData)
    {
        SetupRenderPasses(renderer, renderingData);
        renderer.EnqueuePass(renderPass);
    }
}
```
Pass
```cs
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.RenderGraphModule;
using UnityEngine.Rendering.Universal;

public class ScreenDepthRenderPass : ScriptableRenderPass
{
    private Material material;

    private class CustomPassData
    {
        internal TextureHandle screenColor;
        internal Material overrideMaterial;
    }

    public void Init()
    {
        profilingSampler = new ProfilingSampler("ScreenDepthRenderPass");
        renderPassEvent = RenderPassEvent.AfterRenderingPostProcessing;

        material = new Material(Shader.Find("Shader Graphs/SG_ScreenDepth"));
    }

    public void Setup()
    {
    }

    public void Dispose()
    {
        if (Application.isPlaying)
        {
            Object.Destroy(material);
        }
        else
        {
            Object.DestroyImmediate(material);
        }
    }

    public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
    {
        using (var builder = renderGraph.AddRasterRenderPass<CustomPassData>(passName, out CustomPassData data))
        {
            //passdata
            data.screenColor = frameData.Get<UniversalResourceData>().activeColorTexture;
            data.overrideMaterial = material;

            //read
            //builder.UseTexture(data.screenColor);

            //write
            builder.SetRenderAttachment(data.screenColor, 0, AccessFlags.ReadWrite);

            //process
            builder.SetRenderFunc<CustomPassData>((CustomPassData data, RasterGraphContext context) => ExecutePass(data, context));
        }
    }

    private void ExecutePass(CustomPassData data, RasterGraphContext context)
    {
        //process
        Blitter.BlitTexture(context.cmd, data.screenColor, new Vector4(1, 1, 0, 0), data.overrideMaterial, 0);
    }
}
```

### Monobehavior来控制RendererPass的使用

```cs
﻿using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;

public class ScreenDepthManager : MonoBehaviour
{
    private ScreenDepthRenderPass renderPass;

    private void OnEnable()
    {
        Create();
    }

    private void OnDisable()
    {
        Dispose();
    }

    public void Create()
    {
        renderPass = new ScreenDepthRenderPass();
        renderPass.Init();

        RenderPipelineManager.beginCameraRendering += SetupRenderPass;
    }

    public void Dispose()
    {
        renderPass.Dispose();

        RenderPipelineManager.beginCameraRendering -= SetupRenderPass;
    }

    public void SetupRenderPass(ScriptableRenderContext context, Camera cam)
    {
        renderPass.Setup();
        cam.GetUniversalAdditionalCameraData().scriptableRenderer.EnqueuePass(renderPass);
    }
}
```

### 自定义DrawObject

```cs
```

### 自定义瞄准镜画面

## 疑惑

- RenderingPath 不同渲染路径的深入理解
- 贴花可以用来做什么？原理是什么？
- 场景深度是如何计算的？是什么空间的深度？深度是0-无穷大吗？
- 使用MonoBehaviour和使用RendererFeature来进行RendererPass的控制有什么区别？