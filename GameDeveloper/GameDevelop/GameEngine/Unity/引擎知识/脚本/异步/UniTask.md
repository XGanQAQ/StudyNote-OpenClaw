# 📘 Unity UniTask 笔记

## 一、什么是 UniTask？

**UniTask** 是由 Cysharp 开发的一个针对 Unity 优化的 **轻量级异步任务库**，是 C# 标准 `Task` 的高性能替代方案。

- **核心目标**：在 Unity 中以更少的 GC 开销、更好的性能实现异步编程。
    
- **应用场景**：替代协程 (`Coroutine`) 或 `async/await Task`，用于异步加载、动画控制、网络请求等。
    

---

## 二、为什么要使用 UniTask？

|特性|协程 (`Coroutine`)|C# Task|UniTask|
|---|---|---|---|
|**线程调度**|主线程|线程池|支持主线程|
|**性能**|低 GC，较慢|高 GC，较快|无 GC，高性能|
|**取消控制**|复杂|有 `CancellationToken`|内置取消机制|
|**异常处理**|不便捕获|可 `try/catch`|可 `try/catch`|
|**返回值**|无法返回|可返回|可返回|
|**可等待性**|不能 `await`|可 `await`|可 `await`|
|**与 Unity 集成**|原生|不便|完美（支持 `WaitForSeconds` 等）|

🟢 **一句话总结**：

> UniTask 是 Unity 世界里的 Task —— 快、无GC、支持 await。

---

## 三、基本使用

### 1️⃣ 引入

安装方式（推荐使用 UPM）：

```
https://github.com/Cysharp/UniTask.git?path=src/UniTask/Assets/Plugins/UniTask
```

命名空间：

```csharp
using Cysharp.Threading.Tasks;
```

---

### 2️⃣ 定义与执行异步方法

```csharp
private async UniTask Start()
{
    await ExampleAsync();
    Debug.Log("Task Completed");
}

private async UniTask ExampleAsync()
{
    await UniTask.Delay(1000);  // 延迟1秒
    Debug.Log("Delayed");
}
```

---

### 3️⃣ 与 Unity 生命周期结合

```csharp
private async void Start()
{
    await MoveObjectAsync();
}

private async UniTask MoveObjectAsync()
{
    for (int i = 0; i < 100; i++)
    {
        transform.position += Vector3.forward * 0.1f;
        await UniTask.Yield(); // 每帧等待
    }
}
```

🟡 `UniTask.Yield()` 相当于协程中的 `yield return null;`

---

## 四、常用等待方法

|方法|说明|
|---|---|
|`UniTask.Yield()`|等待一帧|
|`UniTask.Delay(int ms)`|延迟指定毫秒|
|`UniTask.WaitUntil(Func<bool>)`|等待条件成立|
|`UniTask.WaitWhile(Func<bool>)`|等待条件结束|
|`UniTask.WaitForEndOfFrame()`|等待帧结束|
|`UniTask.WaitForFixedUpdate()`|等待物理帧|
|`UniTask.WaitUntilCanceled(CancellationToken)`|等待取消信号|

示例：

```csharp
await UniTask.WaitUntil(() => player.hp <= 0);
Debug.Log("玩家死亡");
```

---

## 五、返回值与异常处理

### ✅ 返回值

```csharp
private async UniTask<int> GetScoreAsync()
{
    await UniTask.Delay(1000);
    return 100;
}

private async void Start()
{
    int score = await GetScoreAsync();
    Debug.Log($"Score = {score}");
}
```

### ⚠️ 异常捕获

```csharp
try
{
    await DoSomethingAsync();
}
catch (Exception e)
{
    Debug.LogError(e);
}
```

---

## 六、与协程的互操作

|操作|示例|
|---|---|
|协程 → UniTask|`await coroutine.ToUniTask()`|
|UniTask → 协程|`yield return myTask.ToCoroutine()`|

示例：

```csharp
IEnumerator Start()
{
    yield return ExampleAsync().ToCoroutine();
}
```

---

## 七、取消机制 (CancellationToken)

```csharp
CancellationTokenSource cts = new CancellationTokenSource();

private async void Start()
{
    try
    {
        await LoadDataAsync(cts.Token);
    }
    catch (OperationCanceledException)
    {
        Debug.Log("任务被取消");
    }
}

private async UniTask LoadDataAsync(CancellationToken token)
{
    await UniTask.Delay(5000, cancellationToken: token);
}
```

取消：

```csharp
cts.Cancel();
```

---

## 八、并发与组合任务

### 1️⃣ 多任务并发执行

```csharp
await UniTask.WhenAll(TaskA(), TaskB(), TaskC());
```

### 2️⃣ 只需等待其中一个完成

```csharp
await UniTask.WhenAny(TaskA(), TaskB());
```

### 3️⃣ 同步顺序执行

```csharp
await TaskA();
await TaskB();
```

---

## 九、Unity 特化功能

UniTask 特别封装了常见 Unity 异步等待：

|等待类型|方法|
|---|---|
|等待 GameObject 销毁|`gameObject.GetAsyncDestroyTrigger()`|
|等待按钮点击|`button.OnClickAsync()`|
|等待Animator播放结束|`await animator.PlayAsync("Run")`|
|等待Scene加载|`await SceneManager.LoadSceneAsync("Main").ToUniTask()`|

---

## 十、性能与注意事项

- ✅ **几乎零GC分配**（相比Task减少装箱/堆分配）
    
- ⚠️ **不要使用 `async void`**，应使用 `async UniTask`
    
- ⚠️ **不要频繁创建新的 `CancellationTokenSource`**
    
- ⚠️ **注意线程上下文**，UniTask默认返回主线程（可用 `.SuppressCancellationThrow()` 处理取消异常）
    

---

## 十一、示例：加载场景 + 动画 + 取消

```csharp
private CancellationTokenSource cts;

private async void Start()
{
    cts = new CancellationTokenSource();

    try
    {
        await LoadSceneAsync(cts.Token);
        await PlayIntroAnimationAsync(cts.Token);
    }
    catch (OperationCanceledException)
    {
        Debug.Log("流程被中断");
    }
}

private async UniTask LoadSceneAsync(CancellationToken token)
{
    await SceneManager.LoadSceneAsync("Main").ToUniTask(cancellationToken: token);
}

private async UniTask PlayIntroAnimationAsync(CancellationToken token)
{
    await animator.PlayAsync("Intro", cancellationToken: token);
}
```

---

## 十二、总结速查表

|功能|对应 UniTask 方法|
|---|---|
|延迟|`UniTask.Delay(ms)`|
|等待条件|`UniTask.WaitUntil()`|
|每帧执行|`UniTask.Yield()`|
|等待协程|`coroutine.ToUniTask()`|
|并行执行|`UniTask.WhenAll()`|
|任一完成|`UniTask.WhenAny()`|
|异步加载场景|`LoadSceneAsync().ToUniTask()`|
|异步等待点击|`button.OnClickAsync()`|
