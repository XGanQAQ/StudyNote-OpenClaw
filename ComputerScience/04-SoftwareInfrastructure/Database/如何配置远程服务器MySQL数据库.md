在远程 Linux 服务器上配置 MySQL 服务器涉及安装 MySQL、进行基本配置并设置远程访问权限。以下是详细步骤：

### 1. 安装 MySQL

在你的远程服务器上使用 SSH 连接进入服务器后，运行以下命令来安装 MySQL 服务器：

```bash
# 更新包管理器
sudo apt update

# 安装 MySQL 服务器（对于Debian/Ubuntu）
sudo apt install mysql-server -y

# 如果使用的是 CentOS/RHEL，使用以下命令
sudo yum install mysql-server -y
```

### 2. 启动并检查 MySQL 服务

确保 MySQL 服务正常运行：

```bash
# 启动 MySQL 服务
sudo systemctl start mysql

# 设置开机自启
sudo systemctl enable mysql

# 检查 MySQL 服务状态
sudo systemctl status mysql
```

### 3. 进行 MySQL 安全设置

MySQL 提供了一个安全脚本，可以帮助你配置安全设置，例如设置 root 密码、删除匿名用户等：

```bash
sudo mysql_secure_installation
```

根据提示完成以下配置：
- 设置 MySQL `root` 用户密码。
- 删除匿名用户。
- 禁止 root 用户远程登录（根据需要）。
- 删除测试数据库。
- 刷新权限表。

### 4. 配置 MySQL 远程访问

如果需要远程连接到 MySQL 服务器，修改 MySQL 配置文件以允许远程访问。编辑 MySQL 的配置文件 `mysqld.cnf`：

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf  # Ubuntu/Debian
# 或者
sudo nano /etc/my.cnf  # CentOS/RHEL
```

找到 `bind-address` 配置项，将其值更改为 `0.0.0.0`：

```ini
bind-address = 0.0.0.0
```

保存并关闭文件后，重启 MySQL 服务：

```bash
sudo systemctl restart mysql
```

### 5. 为远程用户设置权限

登录 MySQL 并为用户设置远程访问权限：

```bash
# 使用 root 用户登录 MySQL
sudo mysql -u root -p
```

在 MySQL 命令行中，创建一个新的用户并授予权限。假设你要创建一个名为 `remote_user` 的用户，密码为 `password`，可以从任何主机访问：

```sql
CREATE USER 'remote_user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'remote_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EXIT;
```

> **注意**：`%` 表示允许任何 IP 地址访问。如果你只希望特定 IP 地址可以访问，则将 `%` 替换为该 IP 地址。

### 6. 配置防火墙

如果你的服务器启用了防火墙，需要允许 MySQL 的端口（默认是 3306）通过：

```bash
# 使用 UFW（Debian/Ubuntu）开放 MySQL 端口
sudo ufw allow 3306

# 使用 firewall-cmd（CentOS/RHEL）开放端口
sudo firewall-cmd --zone=public --add-port=3306/tcp --permanent
sudo firewall-cmd --reload
```

### 7. 测试远程连接

在你的本地机器上，使用以下命令测试连接：

```bash
mysql -h your_server_ip -u remote_user -p
```

输入密码后，如果连接成功说明配置已完成。

### 问题总结
- 记得打开防火墙
- 记得设置的密码要足够安全，不然数据库不通过（仔细查看数据库的反馈）