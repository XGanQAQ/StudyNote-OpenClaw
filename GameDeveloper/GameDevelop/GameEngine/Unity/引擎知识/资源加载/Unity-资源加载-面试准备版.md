**Unity 的资源加载方式**也是面试中常考的知识点（特别是和优化、打包相关），我帮你整理一下复习重点：

---

# 🎯 Unity 资源加载方式总览

## 1. **直接引用（Inspector 绑定 / SerializeField）**

- **原理**：在 Inspector 里直接拖拽引用，Unity 在打包时会自动收集依赖。
    
- **优点**：简单直观，性能好。
    
- **缺点**：耦合度高，不适合动态内容（DLC、热更）。
    
- **应用场景**：固定资源（UI prefab、场景里的角色 prefab）。
    

---

## 2. **`Resources` 文件夹 + `Resources.Load()`**

- **原理**：放在 `Assets/Resources/` 文件夹内的资源会被 Unity 打包进 APK/EXE，可用 `Resources.Load<T>("path")` 动态加载。
    
- **优点**：简单，方便快速调用。
    
- **缺点**：
    
    - 打包时所有 `Resources` 里的资源都会被打进去，无法按需裁剪。
        
    - 资源管理不易追踪，容易造成内存膨胀。
        
- **应用场景**：小项目，快速原型。
    

---

## 3. **AssetBundle**

- **原理**：通过 `BuildPipeline.BuildAssetBundles` 事先打包成独立的资源包，运行时通过 `AssetBundle.LoadFromFile` / `LoadFromMemory` / `LoadFromStream` 加载。
    
- **优点**：
    
    - 可以按需下载和加载，支持 **热更新**。
        
    - 减少包体积。
        
- **缺点**：
    
    - 依赖管理复杂，打包流程麻烦。
        
    - 需要维护版本和缓存策略。
        
- **应用场景**：大型项目、线上版本更新。
    

---

## 4. **Addressables（推荐方式）**

- **原理**：Unity 官方推出的高级资源管理系统（基于 AssetBundle 封装）。通过标签、组策略来管理资源，运行时用 `Addressables.LoadAssetAsync<T>("key")` 动态加载。
    
- **优点**：
    
    - 自动依赖管理。
        
    - 异步加载，性能更好。
        
    - 内置远程更新支持。
        
- **缺点**：
    
    - 学习成本比 Resources 高。
        
- **应用场景**：中大型项目、跨平台项目、需要热更新的项目。
    

---

## 5. **场景加载**

- **SceneManager.LoadScene()**
    
    - 加载整个场景，适合场景切换。
        
- **SceneManager.LoadSceneAsync()**
    
    - 异步加载，不会卡住主线程。
        

---

## 6. **AssetDatabase（仅编辑器可用）**

- **原理**：通过 `UnityEditor.AssetDatabase` API 加载工程内资源。
    
- **用途**：编辑器扩展、开发工具（不能用于打包后的游戏）。
    

---

# 🔄 资源卸载方式

- **Resources.UnloadUnusedAssets()**：卸载未被引用的资源，释放内存。
    
- **Resources.UnloadAsset(Object)**：卸载指定资源。
    
- **AssetBundle.Unload(true/false)**：卸载整个 AssetBundle。
    
- **Addressables.Release(handle)**：释放 Addressables 加载的资源。
    

---

# 🌟 面试常见提问 + 答题思路

1. **问：Resources 和 AssetBundle 的区别？**  
    👉 Resources 简单但不灵活，会全部打包进去；AssetBundle 支持按需加载和热更新，但管理复杂。
    
2. **问：为什么推荐 Addressables？**  
    👉 它是 AssetBundle 的高级封装，提供异步加载、依赖管理、远程更新，适合现代项目。
    
3. **问：怎么防止内存泄漏？**  
    👉 用完的资源要及时释放（Unload / Release），避免长期占用内存。
    