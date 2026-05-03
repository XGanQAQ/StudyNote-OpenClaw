## 如何添加屏幕后处理

### Fullscreen Shader Graph + Full Screnn Renderer Feature

使用FullScreen模板的Shader Graph 编写材质，并为URP 添加 Full Screnn Renderer Feature
将编写的材质设置为其材质

## CRT 效果原理

### 扫描线
- 先获得屏幕uv.y * 屏幕高度
- sin(屏幕uv.y * 屏幕高度)
	- 利用sin函数获得连续重复交替的线
- step(0,屏幕uv.y * 屏幕高度) 
	- 截取出非线性交替的扫描线
- 再将得到的扫描线图与画面混合得到最终画面

## 镜头畸变
- 获得屏幕uv

```cs
float2 uv = i.uv - 0.5;
float dist = dot(uv, uv);
uv *= 1.0 + k * dist;     // 畸变
uv /= zoom;               // Zoom in 防止缩放带来的黑变
uv += 0.5;
```