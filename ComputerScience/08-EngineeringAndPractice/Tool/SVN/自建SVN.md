### 自建SVN服务器的方案

要搭建团队内部的SVN服务器，主要有以下几种方案，各有优缺点，可根据团队规模和技术栈选择：

### 服务器软件选择

#### 1. VisualSVN Server (Windows平台)
- **适合场景**：中小型团队，Windows环境为主
- **特点**：
  - 图形化管理界面，易于上手
  - 集成Apache服务器和LDAP认证
  - 支持HTTPS和Windows域认证
- **安装步骤**：
  1. 下载安装包：https://www.visualsvn.com/server/
  2. 按向导配置仓库路径、端口等
  3. 创建版本库和用户权限
  4. 通过TortoiseSVN客户端连接

#### 2. Apache + SVN (跨平台)
- **适合场景**：技术型团队，需要高度自定义配置
- **特点**：
  - 完全开源，可运行在Linux/Windows
  - 支持多种认证方式（LDAP、数据库等）
  - 性能稳定，适合大规模团队
- **Linux安装示例**：
  ```bash
  # Ubuntu/Debian系统
  sudo apt update
  sudo apt install apache2 subversion libapache2-mod-svn

  # 创建版本库目录
  sudo mkdir -p /var/lib/svn/repos
  sudo svnadmin create /var/lib/svn/repos

  # 配置Apache
  sudo nano /etc/apache2/mods-available/dav_svn.conf
  ```
  在配置文件中添加：
  ```apache
  <Location /svn>
      DAV svn
      SVNParentPath /var/lib/svn
      AuthType Basic
      AuthName "Subversion Repository"
      AuthUserFile /etc/apache2/dav_svn.passwd
      Require valid-user
  </Location>
  ```
  ```bash
  # 创建用户密码
  sudo htpasswd -cm /etc/apache2/dav_svn.passwd username

  # 重启Apache
  sudo systemctl restart apache2
  ```

#### 3. CollabNet Subversion Edge (跨平台)
- **适合场景**：需要企业级功能的团队
- **特点**：
  - 基于Apache，提供Web管理界面
  - 支持版本库镜像和备份
  - 提供活动日志和性能监控
- **安装步骤**：
  1. 下载对应平台的安装包：https://www.collab.net/products/subversion
  2. 按向导完成安装
  3. 通过Web界面配置仓库和用户

#### 4. Docker容器方案
- **适合场景**：技术团队，追求快速部署和隔离性
- **特点**：
  - 一键部署，环境隔离
  - 方便迁移和扩展
- **部署示例**：
  ```bash
  # 使用现有Docker镜像
  docker run -d -p 80:80 -p 3690:3690 \
    -v /path/to/svn/repos:/var/opt/svn \
    garethflowers/svn-server

  # 访问Web管理界面配置
  http://localhost:80/svn-admin
  ```

### 服务器配置最佳实践

1. **存储规划**：
   - 将版本库放在独立分区，避免磁盘满导致的问题
   - 定期备份整个版本库目录

2. **权限管理**：
   - 使用分组管理用户权限
   - 避免全局写权限，按项目分配权限
   - 示例权限配置文件(`authz`)：
     ```
     [groups]
     dev = user1, user2
     admin = admin1

     [/]
     * = r
     @admin = rw

     [project1:/]
     @dev = rw
     ```

3. **性能优化**：
   - 对于大文件较多的项目，启用`fsfs`存储引擎
   - 限制单次提交的文件大小
   - 定期运行`svnadmin verify`检查仓库完整性

4. **访问方式**：
   - 推荐使用HTTPS协议访问
   - 配置Apache时启用KeepAlive以提高性能

### 客户端连接配置

团队成员可通过以下方式连接SVN服务器：

1. **Windows客户端**：
   - 安装TortoiseSVN
   - 右键点击文件夹 → SVN Checkout
   - 输入服务器URL：`https://svn.example.com/svn/repos`

2. **macOS客户端**：
   - 使用命令行工具：`svn checkout https://svn.example.com/svn/repos`
   - 或安装Cornerstone等GUI工具

3. **Linux客户端**：
   - 安装Subversion：`sudo apt install subversion`
   - 命令行操作：`svn checkout https://svn.example.com/svn/repos`

### 后续管理与维护

1. **备份策略**：
   - 定期全量备份：`svnadmin dump /var/lib/svn/repos > repos.dump`
   - 增量备份：记录每次提交的版本号，定期导出变更

2. **用户培训**：
   - 提供基础SVN操作培训
   - 建立团队提交规范（如提交说明格式）

3. **监控与维护**：
   - 监控服务器磁盘空间和性能
   - 定期清理无用的历史版本（需谨慎操作）

根据团队规模和需求，选择合适的方案搭建SVN服务器后，即可实现代码的集中管理和版本控制。对于中小型团队，推荐使用VisualSVN Server或Docker方案快速上手；大型团队或有特殊需求的场景，建议使用Apache + SVN的组合。