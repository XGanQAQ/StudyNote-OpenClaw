# Docker入门

## 使用场景

## 核心概念
容器，一个个独立装有运行依赖的环境，但是不包括操作系统，更为轻量  
镜像，用于复制创建一个容器  
Dockerfile，记录配置Docker的环境的文本

## 安装

## 使用流程

### 创建工程文件夹
构建你的工程

### 编写Dockerfile
Dockerfile记录了Docker容器的配置细节，模拟了环境的配置，用于镜像复制  
如何编写Dockerfile？

### 构建镜像
使用Docker指令来构建镜像  
```bash
docker build -t 镜像名字
```

镜像存储在Docker当中  
查看当前都有哪些镜像
```bash
docker images 
```

### 运行镜像
```bash
docker run 镜像名字
```
### 在另一个环境运行镜像  
#### 方法一：复制镜像文件  

#### 方法二：上传到dockerhub
拉取镜像
```bash
docker pull 镜像链接
```

## DockerDesktop Docker桌面
可视化的Docker软件

## DockerCompose 
组织管理多个应用
