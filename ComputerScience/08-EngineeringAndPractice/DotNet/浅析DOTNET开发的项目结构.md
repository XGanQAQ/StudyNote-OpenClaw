在初学开发DOTNET项目的时候，对于项目中.sln文件和csproj感到疑惑，但是随着不断开发，我大概理解了这些层级的意义
## 主要层级概念

| 层级        | 名称    | 作用               |
| --------- | ----- | ---------------- |
| `.sln`    | 解决方案  | 管理多个项目（项目集合）     |
| `.csproj` | 项目    | 单个编译单元（前端、后端、库等） |
| 文件夹结构     | 模块化目录 | 组织源码与职责模块        |
| 命名空间      | 逻辑命名  | 管理代码引用、作用域划分     |

## 假设开发一个Web应用
在一个sln解决方案之下会有多个文件夹每个文件夹都代表着一个项目，里面有一个csproj文件。
假如我要开发一个前后端分离的个人网站，这个个人网站就是解决方案，其中会有多个部分构成，
前端、后端、共享数据结构、测试等（这些就是代表着一个项目）。

## 如何引用其他同级项目
通过引用用来共享数据结构的项目，让前后端的数据结构得到统一

|方法|可维护性|自动构建支持|类型安全|推荐程度|
|---|---|---|---|---|
|手动复制代码|❌ 差|❌ 无依赖追踪|❌ 易出错|🚫 不推荐|
|`<ProjectReference>`|✅ 高|✅ 支持|✅ 安全强|✅ 推荐|

### 方法1：在 MyProject.Api.csproj 中添加

``` xml

<ItemGroup>

  <ProjectReference Include="..\..\shared\MyProject.Shared\MyProject.Shared.csproj" />

</ItemGroup>

```


### 方法2：使用命令行

``` shell

dotnet add ./backend/MyProject.Api/ reference ./shared/MyProject.Shared/

```

### 发送了什么魔法（引用 Shared 项目时的底层流程）？

当你在 A 项目（比如 `MyProject.Api.csproj`）中引用了 `Shared` 项目，背后发生了以下步骤：
### 🔧 构建阶段：

1. **MSBuild 解析引用关系**：
    
    - 看到 `<ProjectReference>`，知道它需要先构建 `Shared` 项目。
        
2. **构建 Shared 项目**：
    
    - 会编译 `Shared` 中的代码，生成 `.dll`（如 `MyProject.Shared.dll`）。
        
3. **链接 DLL 到主项目**：
    
    - 主项目编译时，会将 `MyProject.Shared.dll` 当作**引用程序集**引入进来。
        
    - 就像你引用了一个第三方 NuGet 包一样，只不过这是你本地写的。
        
4. **类型可用**：
    
    - 主项目可以使用 Shared 中定义的所有 `public` 类型，例如 DTO、枚举等。

## 打包的结果是什么？
在 .NET 中，**打包（build、publish）是针对 `.csproj` 项目文件进行的**，而不是 `.sln` 文件。

---

### `.sln` 是解决方案文件（仅用于组织多个项目）

- `.sln` 本质是一个 **项目列表**，方便开发管理。
    
- 它**不能单独构建或发布成可执行程序**。
    
- 你通常打开 `.sln` 是为了同时管理多个 `.csproj` 项目。
    

---

### `.csproj` 是项目文件（构建的真正入口）

你要构建或发布一个具体的应用（比如前端或后端），**必须指定某个 `.csproj` 文件**：

#### 🔨 构建（build）：

```bash
dotnet build ./backend/MyProject.Api/MyProject.Api.csproj
```

#### 📦 发布（publish）：

```bash
dotnet publish ./frontend/MyProject.Blazor/MyProject.Blazor.csproj -c Release -o ./publish/frontend
dotnet publish ./backend/MyProject.Api/MyProject.Api.csproj -c Release -o ./publish/backend
```

---

### 如果你想打包整个项目怎么办？

你需要分别对前端和后端项目进行 `publish`，因为：

- Web API 和 Blazor 是两个独立的应用程序。
    
- 它们都需要自己的构建、部署步骤。
    

你可以写一个脚本自动执行这些步骤，例如 Bash / PowerShell：

```bash
# build.sh
dotnet publish ./shared/MyProject.Shared.csproj -c Release
dotnet publish ./backend/MyProject.Api.csproj -c Release -o ./publish/backend
dotnet publish ./frontend/MyProject.Blazor.csproj -c Release -o ./publish/frontend

