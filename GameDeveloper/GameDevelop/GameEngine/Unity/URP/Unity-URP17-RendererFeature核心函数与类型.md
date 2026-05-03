# 一、整体理解：RenderGraph 是什么？

在 Unity 的 Universal Render Pipeline 17 里：

RenderGraph 是：

> 一个“声明式渲染调度系统”

你不再：

* 手动申请 RT
* 手动释放 RT
* 手动控制执行顺序

而是：

1. 在 `RecordRenderGraph()` 里声明：

   * 我要读什么
   * 我要写什么
   * 我要创建什么
2. 在 `ExecutePass()` 里真正执行 GPU 命令

---

# 二、RecordRenderGraph 是什么？

```csharp
public override void RecordRenderGraph(
    RenderGraph renderGraph,
    ContextContainer frameData)
```

它的作用是：

> 描述这个 Pass 的资源依赖关系

⚠ 注意：
这里 **不执行 GPU 命令**

---

## 参数 1️⃣：RenderGraph renderGraph

类型：

```csharp
UnityEngine.Rendering.RenderGraphModule.RenderGraph
```

作用：

> 渲染图调度器

你通过它：

* AddRasterRenderPass
* CreateTexture
* 声明依赖
* 设置输出

---

### 常见用法

```csharp
renderGraph.AddRasterRenderPass<PassData>()
renderGraph.CreateTexture()
```

---

## 参数 2️⃣：ContextContainer frameData

类型：

```csharp
UnityEngine.Rendering.ContextContainer
```

作用：

> 当前帧的所有渲染数据集合

你可以从里面拿到：

| 类型                    | 作用        |
| --------------------- | --------- |
| UniversalCameraData   | 相机信息      |
| UniversalResourceData | 当前颜色/深度纹理 |
| UniversalLightData    | 光源数据      |

---

### 示例

```csharp
var resourceData = frameData.Get<UniversalResourceData>();
```

它里面有：

```csharp
resourceData.activeColorTexture
resourceData.activeDepthTexture
```

---

# 三、ExecutePass 是什么？

```csharp
private static void ExecutePass(
    CustomPassData data,
    RasterGraphContext context)
```

这个函数才是真正：

> 执行 GPU 命令的地方

---

## 参数 1️⃣：CustomPassData data

这是你自己定义的类：

```csharp
class CustomPassData
{
    public TextureHandle source;
    public TextureHandle destination;
    public Material material;
}
```

作用：

> 在 Record 阶段收集的数据
> 在 Execute 阶段使用

⚠ RenderGraph 会自动把它传进来

---

## 参数 2️⃣：RasterGraphContext context

类型：

```csharp
UnityEngine.Rendering.RenderGraphModule.RasterGraphContext
```

作用：

> GPU 执行上下文

它包含：

```csharp
context.cmd
context.renderContext
```

---

### context.cmd

类型：

```csharp
CommandBuffer
```

你用它：

```csharp
Blitter.BlitTexture(context.cmd, ...)
context.cmd.SetGlobalTexture(...)
context.cmd.DrawMesh(...)
```

---

### context.renderContext

类型：

```csharp
ScriptableRenderContext
```

一般很少直接用。

---

# 四、执行流程图

假设你写：

```csharp
public override void RecordRenderGraph(...)
{
    using(var builder = renderGraph.AddRasterRenderPass<PassData>())
    {
        passData.source = ...
        builder.UseTexture(source);
        builder.SetRenderAttachment(destination, 0);

        builder.SetRenderFunc((data, context) =>
        {
            ExecutePass(data, context);
        });
    }
}
```

执行顺序是：

```
Frame 开始
↓
RecordRenderGraph（声明资源）
↓
RenderGraph 构建依赖图
↓
调度排序
↓
ExecutePass 被调用
↓
GPU 执行 cmd
```

---

# 五、TextureHandle 是什么？

不是 RTHandle。

是：

> RenderGraph 内部资源引用句柄

你不能：

```csharp
new TextureHandle()
```

必须：

```csharp
renderGraph.CreateTexture()
```

或

```csharp
resourceData.activeColorTexture
```

---

# 六、builder 在做什么？

```csharp
using(var builder = renderGraph.AddRasterRenderPass<PassData>())
```

builder 用来声明：

| API                 | 作用       |
| ------------------- | -------- |
| UseTexture          | 读取依赖     |
| SetRenderAttachment | 写入目标     |
| AllowPassCulling    | 是否允许优化删除 |
| SetRenderFunc       | 设置执行函数   |

---

# 七、为什么要分成 Record 和 Execute？

旧模式：

```csharp
Execute()
{
    Blit()
}
```

URP 不知道你读写什么资源。

---

RenderGraph 模式：

```csharp
Record()
{
    builder.UseTexture(source);
    builder.SetRenderAttachment(dest);
}
```

URP 知道：

* 这个 Pass 读 source
* 写 dest
* 可以自动排序
* 可以自动回收
* 可以自动合并 Pass

---

# 八、对比旧模式 vs 新模式

| 旧 ScriptableRenderPass | 新 RenderGraph |
| ---------------------- | ------------- |
| OnCameraSetup          | CreateTexture |
| Execute                | ExecutePass   |
| RTHandle               | TextureHandle |
| 手动依赖管理                 | 自动依赖图         |

---

# 九、最关键的思维转变

旧模式是：

> 命令式渲染

新模式是：

> 声明式渲染

---

# 十、和你现在体积光项目的关系

你做：

* 屏幕空间 raymarch
* 读取 depth
* 读取 shadow

在 Record 阶段你必须声明：

```csharp
builder.UseTexture(resourceData.activeDepthTexture);
builder.UseTexture(resourceData.activeColorTexture);
```

否则：

RenderGraph 可能会：

* 提前释放
* 不生成资源
* Pass 被裁剪

---

# 十一、总结一句话

### RecordRenderGraph

> “我这一步渲染需要什么资源，输出到哪里”

### ExecutePass

> “真正往 GPU 下发命令”

---

如果你愿意，我可以：

* 给你画一张 **URP17 RenderGraph 执行时序图**
* 或者专门讲：Shadow / Depth 在 RenderGraph 里的生命周期

你现在卡在哪个层级？

* 理论理解？
* 还是具体阴影读不到？
