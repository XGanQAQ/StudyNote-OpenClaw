### SVN是什么？
SVN（Subversion）是一种集中式版本控制系统，诞生于2000年，旨在替代CVS成为更高效的代码管理工具。它采用**中央服务器-客户端**架构，所有文件和版本历史都存储在中央服务器上，用户通过客户端连接服务器进行文件的增删改查。

### SVN与Git的核心区别
| **对比维度**       | **SVN（集中式）**                     | **Git（分布式）**                     |
|--------------------|---------------------------------------|---------------------------------------|
| **架构**           | 中央服务器存储所有历史，客户端依赖联网 | 每个客户端拥有完整仓库副本，支持离线工作 |
| **版本控制单位**   | 基于文件                                | 基于文件快照（commit对象）             |
| **分支成本**       | 高（复制整个目录结构）                | 极低（创建指针）                      |
| **提交方式**       | 必须连接服务器                          | 本地提交，后同步到远程                |
| **典型场景**       | 权限严格的企业级项目                    | 开源协作、快速迭代的项目              |

### 如何使用SVN？（基础操作指南）
#### 1. 安装客户端
- **Windows**：推荐[TortoiseSVN](https://tortoisesvn.net/)（图形界面）
- **macOS**：通过Homebrew安装：`brew install subversion`
- **Linux**：通过包管理器安装：`sudo apt install subversion`（Ubuntu）

#### 2. 基本操作命令
```bash
# 1. 检出项目（从服务器复制到本地）
svn checkout [仓库URL] [本地目录名]
# 示例：svn checkout https://svn.example.com/project/trunk myproject

# 2. 添加新文件/目录
svn add [文件名/目录名]
# 示例：svn add newfile.txt

# 3. 提交修改到服务器
svn commit -m "提交说明"
# 示例：svn commit -m "修复登录Bug"

# 4. 更新本地代码（拉取服务器最新修改）
svn update

# 5. 查看文件状态
svn status
# 状态码说明：M=修改，A=新增，D=删除，?=未版本控制

# 6. 查看历史记录
svn log

# 7. 创建分支
svn copy [源URL] [目标URL] -m "创建分支说明"
# 示例：svn copy https://svn.example.com/project/trunk https://svn.example.com/project/branches/v1.0 -m "创建1.0分支"

# 8. 合并分支修改
svn merge [源分支URL] [目标分支目录]
# 示例：将分支修改合并到trunk
svn merge https://svn.example.com/project/branches/v1.0 .
```

#### 3. 工作流程示例
```bash
# 1. 检出项目
svn checkout https://svn.example.com/myproject

# 2. 修改文件后提交
cd myproject
echo "new content" > readme.txt
svn add readme.txt  # 新增文件时需要add
svn commit -m "添加readme文件"

# 3. 更新代码（多人协作时）
svn update

# 4. 创建分支
svn copy https://svn.example.com/myproject/trunk https://svn.example.com/myproject/branches/feature-x -m "开发X功能"

# 5. 切换到分支工作
svn switch https://svn.example.com/myproject/branches/feature-x
```

### 常见场景解决方案
1. **冲突解决**：当多人修改同一文件时，`svn update`会提示冲突，使用以下命令处理：
   ```bash
   svn resolve --accept [选项] [冲突文件]
   # 选项：working（使用本地修改），theirs-full（使用服务器版本），mine-full（保留本地版本）
   ```

2. **版本回退**：将文件回退到指定版本
   ```bash
   svn merge -r [新版本号]:[旧版本号] [文件路径]
   # 示例：将test.txt回退到版本100
   svn merge -r 101:100 test.txt
   svn commit -m "回退到版本100"
   ```

3. **查看差异**：比较两个版本的差异
   ```bash
   svn diff -r [版本号1]:[版本号2] [文件路径]
   # 示例：比较test.txt在版本100和101的差异
   svn diff -r 100:101 test.txt
   ```

### SVN适用场景
- 企业内部项目，需要严格权限控制
- 文件变更频率低，分支使用较少的项目
- 需要与旧系统兼容的场景

### 注意事项
- **备份重要性**：中央服务器是唯一数据源，需定期备份
- **性能问题**：处理大文件或频繁提交时性能可能不如Git
- **学习曲线**：分支操作和冲突处理相对复杂

通过以上基础操作，你可以快速上手SVN进行代码管理。实际使用时建议结合GUI工具（如TortoiseSVN）提升效率。