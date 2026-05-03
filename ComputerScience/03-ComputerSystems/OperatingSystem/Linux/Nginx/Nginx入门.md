# Nginx入门

## 使用场景

## 安装
### 包安装
方便
### 编译安装
自定义
### Docker安装

## 启动

### 测试是否启动成功
用浏览器访问下面这种格式链接，如果启动成功，可以看到成功的网页  
http://<server_IP_address>/index.nginx-debian.html.

## 配置

## 如何配置文件
配置文件为一个全局文件可以用nginx -V来查看配置文件路径  
功能按块分区

### 常用配置指令
worker_processes 线程数量

include url   
把url下的文件配置都包含进来，这样可以实现分块管理

### 文件管理
- sites-available 存储所有站点的完整配置。
- sites-enabled 只包含当前启用的站点配置（通过符号链接的方式指向 sites-available）。
```bash
ln -s [目标文件或目录] [符号链接的路径]

sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

```