
## 模板项目结构
GanPersonWeb.Client 是前端 UI；
GanPersonWeb 同时作为：
静态资源托管服务（为前端提供 Blazor 文件）；
Web API 服务（通过 REST 提供数据）。

## 可交互渲染模式
MudBlazor需要是可交互渲染模式才可以正常工作
渲染模式再App.razor中定义
设置再MainLayout中设置

默认使用SSR（Server-Side Rendering）但是在SSR下些功能交互无法使用。

在.NET 9之下选择的是@rendermode="InteractiveAuto"（自动渲染模式），
并且每个页面都支持预渲染（无论哪种渲染模式）
