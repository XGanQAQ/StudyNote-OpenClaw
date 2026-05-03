Blazor 是一个用于构建交互式 Web UI 的框架，它支持两种模式：**Blazor Server** 和 **Blazor WebAssembly**。在 Blazor 中，每一个页面或 UI 元素通常都是一个组件（`.razor` 文件），而每个组件在生命周期中会经历一些特定的函数调用，这些被称为“**组件生命周期方法**”。

---

## 🌱 Blazor 组件生命周期函数一览

下面是常用的生命周期函数及其作用：

| 生命周期函数                      | 触发时机                | 作用                                           |
| --------------------------- | ------------------- | -------------------------------------------- |
| `OnInitialized`             | 组件初始化时（只调用一次）       | 用于初始化组件状态，适合执行**同步初始化逻辑**                    |
| `OnInitializedAsync`        | 组件初始化时（异步版本）        | 与 `OnInitialized` 类似，但用于执行**异步操作**（如 API 请求） |
| `OnParametersSet`           | 参数设置或更新时调用（每次参数变更时） | 当父组件传递参数时调用，适合**根据参数更新内部状态**                 |
| `OnParametersSetAsync`      | 同上，异步版本             | 与 `OnParametersSet` 类似，但适用于**异步更新逻辑**        |
| `OnAfterRender`             | 首次或每次渲染完成后调用        | 可用于**DOM 操作**或调用 JavaScript                  |
| `OnAfterRenderAsync`        | 同上，异步版本             | 常用于**首次渲染后的异步初始化**，如 JavaScript interop      |
| `ShouldRender`              | 每次状态变更引起的渲染前调用      | 返回 `false` 可**跳过本次渲染**，用于优化性能                |
| `Dispose`（来自 `IDisposable`） | 组件被销毁时调用            | 用于**释放资源**，比如取消定时器、取消订阅事件等                   |

---

## 🌀 生命周期流程图（简化）

```plaintext
组件创建
  ↓
[OnInitialized / OnInitializedAsync]
  ↓
[OnParametersSet / OnParametersSetAsync]
  ↓
渲染 UI（RenderTree）
  ↓
[OnAfterRender / OnAfterRenderAsync]
  ↓
(后续状态变更时，重复参数更新 → 渲染 → OnAfterRender)
  ↓
组件销毁时 → [Dispose]
```

---

## 🧠 示例代码说明

```razor
@code {
    protected override void OnInitialized()
    {
        Console.WriteLine("组件初始化了（同步）");
    }

    protected override async Task OnInitializedAsync()
    {
        Console.WriteLine("开始异步加载数据...");
        await Task.Delay(1000);
        Console.WriteLine("异步数据加载完成！");
    }

    protected override void OnParametersSet()
    {
        Console.WriteLine("接收到参数！");
    }

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            Console.WriteLine("组件首次渲染完成！");
            await JS.InvokeVoidAsync("console.log", "调用了 JS");
        }
    }

    public void Dispose()
    {
        Console.WriteLine("组件即将销毁，清理资源");
    }
}
```

---

## 🧩 补充说明

- `OnInitialized` / `OnInitializedAsync` 只在**组件第一次创建时调用一次**。
    
- `OnParametersSet` / `OnParametersSetAsync` 在**每次父组件参数变化时**都会调用。
    
- `OnAfterRenderAsync` 中的 `firstRender` 参数是判断**是否首次渲染**的关键。
    
- `Dispose` 方法仅在组件从 UI 中移除或其宿主被销毁时调用，例如使用 `<CascadingValue>` 动态添加/移除组件时。
    

---

如果你是在实际开发中有某些场景想实现，比如：**初始化数据、动态加载内容、避免不必要的重渲染**等，可以告诉我，我可以结合具体场景给你举例。