# 单例 vs 静态类

## 核心区别

| 维度 | 静态类 | 单例 |
|------|--------|------|
| 实例化 | ❌ 不能 new | ✅ 仅允许一次实例 |
| 继承接口 | ❌ 不能 | ✅ 可以 |
| 多态 | ❌ 静态方法无 override | ✅ 可面向接口/基类 |
| 构造函数 | ❌ 不能有实例构造 | ✅ 可以有私有构造 |
| 生命周期 | AppDomain 内常驻 | 可控（懒汉/饿汉/IoC） |
| 单元测试 | 难（无法 mock） | 易（替换实例即可） |

## 代码示例

```csharp
// 静态类：纯工具
public static class MathUtil
{
    public static float Lerp(float a, float b, float t) => a + (b - a) * t;
}

// 单例：可继承接口，方便替换
public interface IAudioService { void Play(string name); }

public sealed class AudioManager : IAudioService
{
    public static IAudioService I { get; private set; } = new AudioManager();
    private AudioManager() { }
    public void Play(string name) { /* ... */ }
}
```

## 结论

- **纯工具/常量** → 静态类
- **需要接口、替换、延迟初始化** → 单例
