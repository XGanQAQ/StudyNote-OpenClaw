# Addressables 的加载模型

## 显式加载
```csharp
var handle = Addressables.LoadAssetAsync<T>(key);

//显式释放
Addressables.Release(handle);
```

## 与 Resources.Load 的区别

- 有句柄
    
- 有引用计数
    
- 有明确 Owner