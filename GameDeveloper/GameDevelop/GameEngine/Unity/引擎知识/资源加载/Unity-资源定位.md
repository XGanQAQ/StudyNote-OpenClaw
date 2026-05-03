Unity 中“资源定位”（即**通过某种标识找到资源并加载**）其实有多种实现方案。它们适用于不同阶段、不同项目规模、不同架构需求。下面我按**工程层级 + 实际使用价值**帮你系统整理一份完整对照表。

---

# 一、Unity 所有资源定位方案总览

|类型|方式|运行时可用|推荐程度|适用项目|
|---|---|---|---|---|
|硬引用|直接拖拽引用|✔|⭐⭐⭐|小项目|
|路径加载|Resources.Load|✔|⭐⭐|原型|
|AssetBundle|路径或名称|✔|⭐⭐⭐⭐|中大型|
|Addressables|AddressKey|✔|⭐⭐⭐⭐⭐|正式项目|
|GUID|AssetDatabase|❌|⭐⭐|编辑器工具|
|InstanceID|内存ID|❌|❌|不可持久化|
|自定义ID|表驱动|✔|⭐⭐⭐⭐⭐|商业项目|

---

# 二、各方案原理 + 优缺点 + 示例

---

## ① 硬引用（Inspector拖拽）

### 原理

Unity 序列化直接保存资源引用。

```csharp
public GameObject prefab;
```

### 优点

✔ 最简单  
✔ 无加载逻辑

### 缺点

❌ 无法动态加载  
❌ 无法做存档引用  
❌ 无法热更新

📌 本质：

> 编译期绑定

---

---

## ② Resources.Load（路径加载）

```csharp
Resources.Load<GameObject>("Enemy/Boss");
```

### 原理

Unity 构建时把 Resources 文件夹打进特殊资源包。

### 优点

✔ 简单  
✔ 支持运行时加载

### 缺点

❌ 无依赖管理  
❌ 无内存控制  
❌ 所有资源被打进包

📌 本质：

> 特殊路径查找表

---

---

## ③ AssetBundle（底层资源包系统）

```csharp
AssetBundle.LoadFromFile(path)
bundle.LoadAsset<GameObject>("Boss");
```

### 原理

Unity 的原生资源分包格式。

### 优点

✔ 支持热更新  
✔ 支持远程加载  
✔ 支持分包

### 缺点

❌ API原始  
❌ 依赖管理要自己做

📌 本质：

> 文件包 + 名称索引

---

---

## ④ Addressables（官方推荐）

```csharp
Addressables.LoadAssetAsync<GameObject>("boss_enemy");
```

### 原理

Unity 在 AssetBundle 之上封装的资源数据库。

内部结构类似：

```
Dictionary<Key, AssetLocation>
```

### 优点

✔ 自动依赖管理  
✔ 自动缓存  
✔ 支持远程更新  
✔ 异步加载

### 缺点

❌ 初学配置复杂

📌 本质：

> 资源数据库系统

---

---

## ⑤ GUID（编辑器资源唯一ID）

```csharp
AssetDatabase.GUIDToAssetPath(guid);
```

### 优点

✔ 永久唯一

### 缺点

❌ 运行时不可用

📌 只用于：

- 编辑器工具
    
- 自动生成配置
    
- 资源扫描
    

---

---

## ⑥ InstanceID（运行时对象ID）

```csharp
obj.GetInstanceID();
```

### 特点

- 每次运行都会变
    
- 只在当前进程有效
    

❌ 不能存档  
❌ 不能网络同步

📌 只用于：

- 内存对象管理
    

---

---

## ⑦ 自定义资源ID系统（商业项目标配 ⭐）

这是大型项目真正使用的方案。

### 原理

资源 → 自定义ID → 查表 → 加载

例如：

```
weapon_ak47 → AddressableKey → prefab
```

### 存档数据

```json
{
  "weapon": "weapon_ak47"
}
```

---

# 三、资源定位方案架构层级图（核心理解）

```
最底层
│
├── 文件路径
│
├── AssetBundle
│
├── Addressables
│
├── 自定义资源ID系统 ⭐⭐⭐
│
└── 游戏逻辑调用
```

越往上：

✔ 越抽象  
✔ 越安全  
✔ 越可扩展

---

# 四、真正商业项目资源定位架构（推荐模板）

```
GameLogic
   ↓
ResourceID
   ↓
ResourceManager
   ↓
Addressables
   ↓
AssetBundle
```

优势：

- 可以替换底层加载方式
    
- 可以统一资源管理
    
- 可以统计引用
    
- 可以做缓存策略
    

---

# 五、如何选择（按项目规模）

### 小游戏 / Demo

👉 直接拖拽引用

---

### 中型项目

👉 Addressables

---

### 大型项目 / 商业项目

👉 自定义ID + Addressables

---

# 六、存档 / 网络同步推荐方案（重要）

无论项目大小：

> 永远不要保存 Unity Object 引用  
> 永远保存资源ID

示例：

```csharp
public string weaponId;
```

---

# 七、终极总结（核心原则）

Unity 资源定位本质只有两种：

```
① 直接引用（硬引用）
② 间接索引（ID查找）
```

所有系统（Resources / Addressables / AssetBundle）

本质都是：

> ID → 查表 → 资源