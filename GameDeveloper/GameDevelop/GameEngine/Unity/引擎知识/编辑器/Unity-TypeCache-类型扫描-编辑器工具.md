# TypeCache —— Unity 类型扫描笔记

## 一、TypeCache 是什么

**TypeCache** 是 Unity 在 **Editor 环境** 提供的 **类型索引系统**。

> Unity 在脚本导入 / 重新编译时，  
> **提前扫描并缓存所有类型的“继承 / 接口 / Attribute 关系”**，  
> 供编辑器工具高速查询。

### 一句话理解

> **TypeCache = Unity 帮你做好的“类型数据库”**

---

## 二、TypeCache 解决了什么问题

传统反射扫描的问题：

|问题|Reflection|
|---|---|
|性能|慢|
|GC|高|
|Editor 卡顿|容易|
|可维护性|差|

TypeCache 的优势：

|项目|TypeCache|
|---|---|
|查询速度|⭐⭐⭐⭐⭐|
|GC|极低|
|使用复杂度|低|
|适合 Editor 工具|✔|

👉 **Unity 官方推荐：Editor 类型扫描一律用 TypeCache**

---

## 三、TypeCache 的使用前提（重要）

- ✔ 仅在 **Editor 环境**
    
- ✔ 位于 `UnityEditor` 命名空间
    
- ❌ 不能在 Runtime（Build 后）使用
    

```csharp
#if UNITY_EDITOR
using UnityEditor;
#endif
```

---

## 四、最常用的 3 种扫描方式（核心）

### 1️⃣ 扫描「带某个 Attribute 的类型」

```csharp
var types = TypeCache.GetTypesWithAttribute<MyAttribute>();
```

**适用场景**

- 自动注册
    
- 单例标记
    
- 模块声明
    

---

### 2️⃣ 扫描「继承某个基类的类型」

```csharp
var types = TypeCache.GetTypesDerivedFrom<BaseClass>();
```

**适用场景**

- Mono 基类
    
- Service 基类
    
- 框架扩展点
    

---

### 3️⃣ 扫描「实现某接口的类型」

```csharp
var types = TypeCache.GetTypesDerivedFrom<IMyInterface>();
```

⚠ 接口也使用 `GetTypesDerivedFrom`

---

## 五、TypeCache 返回的是什么

```csharp
IEnumerable<Type>
```

每一个元素都是：

```csharp
System.Type
```

你可以对它做的事：

- `type.Name`
    
- `type.FullName`
    
- `Activator.CreateInstance(type)`
    
- `type.GetCustomAttributes(...)`
    

---

## 六、TypeCache 在架构中的典型用法

### 场景 1：自动发现 Service（Editor）

```csharp
var services = TypeCache.GetTypesDerivedFrom<IAppService>();

foreach (var type in services)
{
    if (type.IsAbstract) continue;
}
```

---

### 场景 2：单例管理器 / Viewer

```csharp
var singletons = TypeCache.GetTypesWithAttribute<SingletonAttribute>();
```

展示：

- 类型名
    
- Scope（Scene / Game / App）
    
- 是否已实例化
    

---

### 场景 3：架构约束检查（高级）

- 扫描所有 Service
    
- 检查是否引用 `UnityEngine.Object`
    
- 发现非法依赖立即报错
    

---

## 七、TypeCache vs 反射（对比总结）

|维度|TypeCache|Reflection|
|---|---|---|
|Editor 使用|✔ 推荐|❌|
|Runtime 使用|❌|✔|
|性能|极高|较低|
|使用复杂度|低|高|

### 结论

> **Editor 用 TypeCache  
> Runtime 用显式注册 / 代码生成**

---

## 八、Runtime 不能用 TypeCache，该怎么办？

### ✅ 正确做法 1（推荐）

**Editor 扫描 → 生成代码**

```text
TypeCache 扫描
   ↓
生成 AppServices.cs
   ↓
Runtime 直接调用
```

---

### ✅ 正确做法 2

- TypeCache 仅用于：
    
    - Editor Window
        
    - Debug / Viewer
        
    - 校验工具
        

---

### ❌ 不推荐

- Runtime 反射扫描
    
- 每次启动动态发现
    

---

## 九、常见坑 & 注意事项

### ⚠ 1. 抽象类也会被扫到

```csharp
if (type.IsAbstract) continue;
```

---

### ⚠ 2. Editor 脚本要放在 Editor 文件夹

否则：

- 引用 `UnityEditor` 会编译失败
    

---

### ⚠ 3. TypeCache 结果在编译后才更新

- 新增类
    
- 改 Attribute
    

👉 需要脚本重新编译

---

### ⚠ 4. TypeCache 不保证顺序

- 不要依赖返回顺序
    
- 如需顺序，自己排序
    

---

## 十、推荐使用规范（经验总结）

### ✔ 推荐

- 用 Attribute 标记“参与扫描”的类型
    
- Editor 中扫描
    
- Runtime 中显式调用
    

### ❌ 不推荐

- 把 TypeCache 当 IOC 容器
    
- Runtime 依赖类型扫描
    
- 大量逻辑放在 Editor 扫描结果里
    

---

## 十一、TypeCache 的“心智模型”（重要）

```
脚本导入 / 编译
    ↓
Unity 构建 TypeCache
    ↓
Editor 工具查询
    ↓
生成 / 展示 / 校验
```

---

## 十二、一句话总结（记住这句）

> **TypeCache 是“编辑器的眼睛”，  
> 不是“运行时的大脑”。**

---

如果你愿意，下一步我可以帮你把这份笔记**直接转成：**

- 🔹 一个 `TypeCacheHelper` 工具类
    
- 🔹 一个「单例 / Service 扫描 + 可视化」EditorWindow
    
- 🔹 或一套 **架构规则检查器**
    

你更想把哪一个真正落地到项目里？