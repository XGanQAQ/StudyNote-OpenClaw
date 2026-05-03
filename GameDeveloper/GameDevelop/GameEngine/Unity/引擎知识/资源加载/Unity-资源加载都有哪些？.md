Unity 的 **资源加载（Asset Loading）** 主要有以下几类方式，取决于资源的存储位置、打包方式和运行时需求：

---

## 一、编辑器直接引用（静态加载）

- **方式**：在 Inspector 里拖拽资源到脚本字段，或直接引用到场景 / Prefab。
    
- **调用**：Unity 在构建时会将这些资源自动打进包里，运行时直接加载。
    
- **特点**：
    
    - 简单直观。
        
    - 缺点：无法按需加载，全部在场景切换时一次性加载，内存占用大。
        

---

## 二、`Resources` 目录加载

- **方式**：将资源放到 `Assets/Resources` 文件夹下。
    
- **调用**：
    
    ```csharp
    var prefab = Resources.Load<GameObject>("Prefabs/MyPrefab");
    var instance = Instantiate(prefab);
    ```
    
- **特点**：
    
    - 支持字符串路径动态加载。
        
    - 缺点：所有 `Resources` 下的资源会整体打包到游戏里，无法精细控制，容易导致包体膨胀。
        

---

## 三、`AssetBundle` 资源包

- **方式**：手动打包资源到 AssetBundle 文件，运行时再加载。
    
- **调用**：
    
    ```csharp
    var bundle = AssetBundle.LoadFromFile("path/to/bundle");
    var prefab = bundle.LoadAsset<GameObject>("MyPrefab");
    ```
    
- **特点**：
    
    - 适合热更新、可下载内容（DLC）、分包加载。
        
    - 缺点：依赖管理复杂，需要打包流程和版本管理。
        

---

## 四、`Addressables` 系统（推荐现代做法）

- **方式**：Unity 官方推荐的资源管理框架，基于 AssetBundle 封装。
    
- **调用**：
    
    ```csharp
    Addressables.InstantiateAsync("MyPrefab");
    ```
    
- **特点**：
    
    - 异步加载、自动管理依赖。
        
    - 支持远程服务器资源下载。
        
    - 支持引用计数和内存回收。
        
    - 缺点：学习成本高，运行时依赖 `Addressables` 包。
        

---

## 五、`StreamingAssets` 文件

- **方式**：资源放在 `Assets/StreamingAssets`，构建时原样拷贝到目标平台。
    
- **调用**：
    
    ```csharp
    string path = Path.Combine(Application.streamingAssetsPath, "data.json");
    string json = File.ReadAllText(path);
    ```
    
- **特点**：
    
    - 不会被 Unity 压缩，原封不动存储。
        
    - 适合配置文件、视频、外部数据。
        
    - 缺点：不能直接用 Unity API 加载（如 Prefab），需要自己写解析逻辑。
        

---

## 六、`PersistentDataPath` / 外部存储

- **方式**：游戏运行时写入/下载到 `Application.persistentDataPath`。
    
- **用途**：存档文件、动态下载资源、补丁。
    
- **调用**：需要配合 `AssetBundle` 或自定义格式。
    

---

## 七、`Scene` 加载（间接资源加载）

- **方式**：场景本身作为一个资源包，加载场景时 Unity 会加载场景内引用的所有资源。
    
- **调用**：
    
    ```csharp
    SceneManager.LoadScene("MyScene");
    ```
    
- **特点**：
    
    - 简单直接。
        
    - 缺点：无法按需单独加载场景里的某个 Prefab。
        

---

## 八、Web/外部数据加载

- **方式**：通过 `UnityWebRequest` 下载文件（比如 JSON、图片、AssetBundle）。
    
- **调用**：
    
    ```csharp
    var request = UnityWebRequestTexture.GetTexture(url);
    await request.SendWebRequest();
    var texture = DownloadHandlerTexture.GetContent(request);
    ```
    
- **特点**：
    
    - 灵活，可与 CDN/服务器结合。
        
    - 常用于热更和在线内容。
        

---

✅ **总结**：

- **小项目/原型** → 直接引用 / `Resources`
    
- **正式项目（本地资源）** → Addressables（推荐）
    
- **需要热更/DLC** → AssetBundle 或 Addressables
    
- **外部配置/视频/原始数据** → StreamingAssets
    
- **运行时下载/存档** → PersistentDataPath + UnityWebRequest