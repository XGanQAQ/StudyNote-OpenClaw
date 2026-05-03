## 一、Blit 的基本定义

**Blit** 是 “**Bit Block Transfer**” 的缩写。  
简单来说，它的作用就是：

> **把一张 Render Texture（渲染纹理）复制到另一张纹理上，可以在复制的过程中执行一个 Shader（材质）操作。**

---

## 二、在 URP 中的用途

在 URP（尤其是自定义渲染流程、后处理、自定义 Renderer Feature）中，`Blit` 常用于：

|用途|说明|
|---|---|
|**后处理效果**|把相机的渲染结果复制到一张中间纹理上，然后通过自定义 Shader 处理（例如：Bloom、模糊、CRT 效果）|
|**屏幕到屏幕拷贝**|把渲染结果从一张 RT 复制到另一张 RT（比如 `_CameraColorTexture` → `_AfterPostProcessTexture`）|
|**中间过渡**|在多阶段渲染（多个 pass）中，用 Blit 把上一个阶段的结果作为下一个阶段的输入|

---

## 三、常见的两种 Blit 用法

### 1️⃣ 传统的 `Blit` 调用

```csharp
cmd.Blit(source, destination, material);
```

- `source`: 输入纹理（RenderTarget）
    
- `destination`: 输出纹理（RenderTarget）
    
- `material`: 可选，用于执行特定的 shader
    

⚙️ 实际上这会：

- 设置目标纹理为 `destination`
    
- 把 `source` 绑定成 `_MainTex`
    
- 绘制一个全屏四边形（Fullscreen Quad）
    

如果提供了 `material`，则执行 `material` 的第一个 Pass。

---

### 2️⃣ 新的 `Blitter.BlitCameraTexture`

从 **URP 12+**（Unity 2021 起）开始，Unity 推荐使用：

```csharp
Blitter.BlitCameraTexture(cmd, source, destination, material, passIndex);
```

或：

```csharp
Blitter.Blit(cmd, source, destination, material, passIndex);
```

因为旧的 `cmd.Blit()` 已经被标记为**性能较差且将被弃用**。

`Blitter` 内部使用一个全屏三角形而不是四边形，更高效、无缝隙。

---

## 四、Blit 在自定义 Renderer Feature 中的典型流程

假设你写了一个自定义后处理：

```csharp
class CustomPostProcessPass : ScriptableRenderPass
{
    private Material material;
    private RenderTargetIdentifier source;
    private RenderTargetHandle tempTexture;

    public void Setup(RenderTargetIdentifier src)
    {
        source = src;
    }

    public override void Execute(ScriptableRenderContext context, ref RenderingData renderingData)
    {
        var cmd = CommandBufferPool.Get("CustomPostProcess");

        // 1. 获取临时RT
        cmd.GetTemporaryRT(tempTexture.id, renderingData.cameraData.cameraTargetDescriptor);

        // 2. Blit source → temp (执行Shader)
        Blit(cmd, source, tempTexture.Identifier(), material);

        // 3. Blit temp → source (写回结果)
        Blit(cmd, tempTexture.Identifier(), source);

        context.ExecuteCommandBuffer(cmd);
        CommandBufferPool.Release(cmd);
    }
}
```

流程图大致如下：

```
CameraColorTarget (源)
      ↓  Blit + Shader
临时RT
      ↓  Blit回去
CameraColorTarget (更新后的结果)
```

---

## 五、性能与注意点

|问题|说明|
|---|---|
|**多次 Blit 会增加带宽消耗**|每次 Blit 都涉及 GPU 内存读写（texture copy），所以要尽量减少中间纹理数量|
|**必须正确匹配 RenderTarget 格式**|否则可能会出现黑屏或格式不匹配错误|
|**不要在 RenderPass 内部直接用 Graphics.Blit()**|在 SRP（URP/HDRP）中必须用 CommandBuffer 的 Blit 或 Blitter 调用|

---

## 六、一句话总结

> 💡 **Blit 是一种“把画面拷贝并可附带 shader 处理”的操作。**  
> 在 URP 中，它通常被用来实现后处理效果或阶段性渲染过渡。

