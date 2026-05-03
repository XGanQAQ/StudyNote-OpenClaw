Unity 的 **`AssetReference`** 是 Addressables 系统提供的一个核心类，用来**以引用方式指向资源，而不是直接持有资源对象**。它本质上是一个**可序列化的资源地址句柄**，用于运行时动态加载资源。

---

# 一、简单理解一句话

👉 **AssetReference = 一个可序列化的资源地址指针（GUID + Addressable Key 封装）**

它不是资源本身，而是  
✔ 资源定位信息  
✔ 加载入口  
✔ 生命周期管理接口

---

# 二、为什么需要 AssetReference

如果你直接写：

```csharp
public GameObject prefab;
```

问题：

- 会变成硬引用
    
- 资源会被打包进场景依赖
    
- 无法按需加载/卸载
    
- 不利于热更新
    
- 无法跨包加载
    

而使用：

```csharp
public AssetReference prefabRef;
```

优势：

- 不直接依赖资源
    
- 可以异步加载
    
- 可以动态释放
    
- 支持远程资源
    
- 支持热更新
    

---

# 三、AssetReference内部原理（底层结构）

AssetReference 内部其实只存：

```
GUID（字符串）
```

Unity通过GUID查找Addressables资源定位表：

```
AssetReference
     ↓
GUID
     ↓
Addressables Resource Locator
     ↓
资源路径/Bundle
     ↓
加载Asset
```

---

# 四、核心API

最常用的加载方法：

---

## 1️⃣ 异步加载资源

```csharp
var handle = prefabRef.LoadAssetAsync<GameObject>();
await handle.Task;
GameObject obj = handle.Result;
```

---

## 2️⃣ 实例化Prefab

```csharp
var handle = prefabRef.InstantiateAsync();
await handle.Task;
GameObject obj = handle.Result;
```

---

## 3️⃣ 释放资源

```csharp
prefabRef.ReleaseAsset();
```

或

```csharp
Addressables.Release(handle);
```

---

# 五、和 Addressables.LoadAssetAsync 的区别

### 不用 AssetReference

```csharp
Addressables.LoadAssetAsync<GameObject>("PlayerPrefab");
```

问题：

- key是字符串
    
- 不安全
    
- 容易拼写错误
    
- 无法Inspector拖拽
    

---

### 使用 AssetReference

```csharp
[SerializeField] AssetReference playerPrefab;
```

优点：

- Inspector可拖拽
    
- 自动校验类型
    
- 不会写错key
    
- 可序列化存储
    

---

# 六、AssetReference类型变体

Unity提供了强类型版本：

|类型|用途|
|---|---|
|AssetReference|任意资源|
|AssetReferenceGameObject|只能引用Prefab|
|AssetReferenceSprite|只能引用Sprite|
|AssetReferenceT|泛型自定义|

例如：

```csharp
public AssetReferenceGameObject enemyPrefab;
```

Inspector里只能拖Prefab。

---

# 七、和 GUID / AddressableKey 的关系（重要）

三者关系如下：

```
资源文件.meta
     ↓
GUID（唯一ID）
     ↓
Addressables系统生成
     ↓
Addressable Key（可读字符串）
```

AssetReference 存的是：

> GUID（不是Key）

加载时 Addressables 会自动把 GUID 转换成资源位置。

---

# 八、使用场景（推荐使用）

以下情况强烈建议用 AssetReference：

✔ 配置表里引用资源  
✔ ScriptableObject配置引用资源  
✔ 存档系统记录资源ID  
✔ 技能系统引用特效  
✔ UI配置引用图标  
✔ 动态加载怪物Prefab

---

# 九、不推荐使用场景

❌ 永远不会卸载的核心资源  
（例如常驻UI字体）

因为：

- AssetReference加载有开销
    
- Addressables查表成本
    

这些资源直接硬引用更好。

---

# 十、你当前项目里应该怎么用（针对你）

你现在在做：

> 配置ID → 找资源（SO / Prefab）

最佳结构：

```
配置表存：
    string assetID

运行时：
    assetManager.Load(assetID)
```

而配置表中如果需要可视化引用资源：  
👉 就使用 **AssetReference**

---

# 十一、架构级最佳实践（高级建议）

推荐统一封装一层：

```csharp
public struct AssetHandle<T>
{
    public AssetReference reference;
}
```

所有资源加载都走：

```
GameAssetSystem
```

而不是直接调用 Addressables。

这样以后：

- 换资源系统
    
- 做缓存
    
- 做预加载
    
- 做统计
    

都不用改业务代码。

---

# 总结（核心理解版）

**AssetReference 本质就是一个序列化资源定位器。**

它的定位不是资源，而是：

> 一个可拖拽、可序列化、可动态加载的资源句柄