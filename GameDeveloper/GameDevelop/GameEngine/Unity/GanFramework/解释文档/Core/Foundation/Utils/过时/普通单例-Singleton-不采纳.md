纯 C# 单例，不依赖 `MonoBehaviour` **线程安全、懒加载、可扩展**的版本

```cs
using System;

namespace Core
{
    /// <summary>
    /// 线程安全的普通单例基类。
    /// 用于不依赖 Unity 生命周期的全局管理类，例如配置、数据缓存、逻辑系统等。
    /// </summary>
    /// <typeparam name="T">单例类型。</typeparam>
    public abstract class Singleton<T> where T : Singleton<T>, new()
    {
        // Lazy 确保线程安全的延迟初始化
        private static readonly Lazy<T> _instance = new(() => new T());

        /// <summary>
        /// 获取单例实例。
        /// </summary>
        public static T Instance => _instance.Value;

        /// <summary>
        /// 标记是否已初始化（可用于自定义初始化逻辑）
        /// </summary>
        public static bool IsInitialized => _instance.IsValueCreated;

        /// <summary>
        /// 受保护的构造函数，防止外部实例化。
        /// </summary>
        protected Singleton() { }

        /// <summary>
        /// 可选的初始化逻辑。
        /// 子类可重写此方法用于初始化资源。
        /// </summary>
        public virtual void Initialize() { }

        /// <summary>
        /// 可选的释放逻辑。
        /// 子类可重写此方法用于释放资源。
        /// </summary>
        public virtual void Dispose() { }
    }
}

```