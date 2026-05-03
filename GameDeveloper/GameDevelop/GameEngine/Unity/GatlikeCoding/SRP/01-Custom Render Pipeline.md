

SRP 是 Unity 提供的一个高级框架，它允许你使用 **C# 脚本** 来完全控制 Unity 的渲染过程。
## 1. A new Render Pipeline

over

### 1.1 Project Setup

在创建好自己编写的Scriptable Render Pipeline Asset 的时候，当当把Graphics project setting 修改为自己编写的仍然无法修改为你自己写的，还需要，修改Quality 下的 Rendering 的 Render Pipeline Asset。

### 1.2 Pipeline Asset

Pipeline Asset 设置各种选项

### 1.3 Render Pipeline Instance

## 2. Rendering

RP will pass a context to provides a connection to engine, which we can use for rendering.
It also pass a camera array

### 2.1 Camera Renderer

定义一个相机类 to dedicated to rendering one camera，并用他的Render方法with a context and a camera parameter,  
In pipeline to create the instance of the renderer, and use it to render all cameras in a loop
The camera renderer is like URP, in the future, we can use different camera to render different codition. But now we render all cameras the same way.

### 2.2 Drawubg the Skybox

The function - cameraRenderer.Render is to draw all geometry. so we define a method - DrawVisibleGemotry for clarity.

the context are buffered. we need to submit the queued workd for execution.

To correctly render the skybox—and the entire scene—we have to set up the view-projection matrix.

### 2.3 Command Buffers

We need a buffers to draw the other geometry

We can use command buffers to inject profiler samples

To execute the buffer, invoke `ExecuteCommandBuffer` 

### 2.4 Clearing the Render Target

invoking `ClearRenderTarget` to get ri of its old content

modify the express of line, the work will different in frame debugger.

### 2.5 Culling

We define a function to culling, and we use `ScriptableCullingParameters` to keep track of multiple camera settings and matrices.

Culling is done by invoking `cull` on the context. So we produces a `CullingResult` struct.

### 2.6 Drawing Geometry

We need the structs
- **DrawingSettings**
	- Supply drawing settings
	- **ShaderTagID**
		- indicate which kind of shader passes are allowed
- **FilteringSettings**
	- Supply filtering settings
	-  indicate which render queues are allowed
		- [RenderQueueRange](http://docs.unity3d.com/Documentation/ScriptReference/Rendering.RenderQueueRange.html).all
- **SortingSettings**
	- Supply the order to render object
	- criteria = [SortingCriteria](http://docs.unity3d.com/Documentation/ScriptReference/Rendering.SortingCriteria.html).CommonOpaque
		- force a specific draw order by setting the `criteria` property of the sorting settings

### 2.7 Drawing Opaque and Transparent Geometry Separately

Transparent geometry does not write to the depth buffer, causing the skybox overwrites it

To fix this, we modify the filteringSettings to RenderQueueRange.opaque.
After **drawing the skybox**, we assign new sorting, drawing, and filtering settings, then use `drawRenderers` to render transparent geometry.

## 3 Editor Rendering

We use the Error Material to render the unsupported shaders.
To improve class organization, we use partial class and `#if UNITY_EDITOR` to let the unsupported shaders is be rendered only  in the editor.

Last we add the code to draw gizmos and UI

The UI need change canvas model from screen space-overlay to screen space-Camera and using the main camera as its Render Camera.
I understand that the different bettwen overlay and Camera. overlay is use the editor overlay render to render ui at last. camera is use the setting camera's setting to render ui

## 4 Multiple Cameras

### 4.1 Two Cameras

we duplicate the main camera, rename it to Secondary Camera.

At first, **the render work of two cameras in Frame Debugger is merged** in a same scope.
To separate them, we define a function to rename the defaut name by the object name

### 4.2 Dealing with Changing Buffer Names

Because we use different name for samples and their buffer bettwen Begin Sample and End Smaple

To fix this, we take advantage of `#if UNITY_EDITOR`

for we do not get the 100 bytes of allocation, we wrap the camera name retrieval in a profiler sample named Editor Only

### 4.3 Layers

>[!question] Unity的相机组件的参数都有什么用？

We configured the culling mask setting, and make the Secondary Camera renders last.

### 4.4 Clear Flag

we want to combine the results of both cameras. So we defined the CameraClearFlags to setting the clear.


>[!question] 这些各种各样的Settings都是起什么作用？
>这些 `Settings` 对象共同协作，为 `context.DrawRenderers` 命令提供了完整的上下文信息：
>- **`SortingSettings`** 决定了**绘制顺序**。
>- **`DrawingSettings`** 决定了**如何绘制**（使用哪个着色器 Pass，是否进行批处理/实例化）。
>- **`FilteringSettings`** 决定了**绘制哪些对象**（基于渲染队列或 Layer）。
>通过组合和调整这些 `Settings`，你可以灵活地实现各种渲染策略，例如
>- 先绘制所有不透明物体（从近到远），再绘制所有透明物体（从远到近）
>- 在不同的 Pass 中绘制物体，实现深度预通道、阴影图生成等。
>- 控制渲染性能优化手段（动态合批、GPU 实例化）的启用与否。
>理解这些 `Settings` 的用法是掌握 SRP 中渲染流程控制的关键一步。


