## ✅ XMake 是什么？

**XMake** 是一个基于 Lua 语言构建的、**轻量、跨平台、灵活的 C/C++ 构建工具**，类似于 CMake、Meson 等工具。它的主要特点有：

- **易用性强**：使用 Lua 脚本定义构建规则，语法直观。
    
- **跨平台支持好**：支持 Windows、Linux、macOS、Android、iOS、Wasmer 等。
    
- **原生构建系统整合**：支持 MSVC、gcc、clang、emcc、xcodebuild 等。
    
- **包管理支持**：内置 xrepo 包管理器，可以一行命令拉取和使用依赖库。
    
- **无需依赖第三方工具**：XMake 自带构建系统，不像 CMake 需要依赖 Make/Ninja。
    

---

## 🚀 如何快速上手

### 步骤一：安装 XMake

#### Windows：

```bash
choco install xmake     # 使用 Chocolatey
scoop install xmake     # 使用 Scoop
```

#### macOS：

```bash
brew install xmake
```

#### Linux：

```bash
curl -fsSL https://xmake.io/shget.text | bash
```

---

### 步骤二：创建项目

```bash
xmake create -l c++ -t console my_project
cd my_project
xmake
xmake run
```

说明：

- `-l c++` 指定语言为 C++（也支持 c, objc, swift 等）
    
- `-t console` 创建控制台程序
    
- `xmake` 编译项目
    
- `xmake run` 运行项目
    

---

### 步骤三：查看构建脚本

`xmake.lua` 示例：

```lua
add_rules("mode.debug", "mode.release")

target("my_project")
    set_kind("binary")
    add_files("src/*.cpp")
```

---

## 📌 常用操作简单总结

|操作|命令|说明|
|---|---|---|
|创建新项目|`xmake create -l c++ -t console name`|支持多种模板和语言|
|构建项目|`xmake`|编译当前目录下的项目|
|运行可执行文件|`xmake run`|自动执行刚刚编译的二进制|
|清理构建缓存|`xmake clean`|类似于 `make clean`|
|添加第三方库|`xrepo install zlib`|使用内置包管理器安装依赖|
|配置编译模式|`xmake f -m release`|设置为 Release 模式|
|查看帮助文档|`xmake --help`|显示命令行帮助|
|使用 VS 编译|`xmake f --toolchain=msvc`|设置使用 MSVC 工具链|
|切换平台（如交叉编译）|`xmake f -p cross -a arm64`|支持交叉编译配置|
|打包可执行文件与依赖|`xmake package`|生成压缩包|
