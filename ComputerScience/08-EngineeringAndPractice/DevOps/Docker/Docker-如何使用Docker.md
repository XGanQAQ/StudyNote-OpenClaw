Docker 是一个容器化平台，可以帮助开发者构建、运行、测试和部署应用程序。Docker 的主要优点是轻量级、快速、易于管理、跨平台和支持应用隔离。以下是 Docker 的基础使用教程：

### 1. 安装 Docker
   - 在 [Docker 官方网站](https://www.docker.com/get-started/)下载并安装 Docker。
   - 安装完成后，可以使用 `docker --version` 命令来检查是否安装成功。

### 2. Docker 基本概念
   - **镜像 (Image)**: 应用程序的只读模板，用来创建容器。
   - **容器 (Container)**: 镜像的运行实例，独立运行的环境。
   - **Dockerfile**: 构建 Docker 镜像的配置文件。
   - **仓库 (Repository)**: 用来存放镜像的地方，类似 Git 仓库。常用的有 Docker Hub。

### 3. Docker 基本命令
   - **运行镜像并创建容器**：`docker run [选项] 镜像`
     - 示例：`docker run hello-world`
     - `hello-world` 是官方提供的一个简单测试镜像。
   
   - **查看运行中的容器**：`docker ps`
     - 查看所有容器（包括停止的容器）：`docker ps -a`
   
   - **停止容器**：`docker stop 容器ID或名称`
   
   - **删除容器**：`docker rm 容器ID或名称`
   
   - **查看所有镜像**：`docker images`
   
   - **删除镜像**：`docker rmi 镜像ID或名称`

### 4. 使用 Dockerfile 创建镜像
   Dockerfile 是一个文本文件，用于定义构建镜像的步骤。
   
   **Dockerfile 示例**
   ```Dockerfile
   # 使用基础镜像
   FROM ubuntu:latest

   # 安装软件包
   RUN apt-get update && apt-get install -y nginx

   # 暴露端口
   EXPOSE 80

   # 容器启动时运行命令
   CMD ["nginx", "-g", "daemon off;"]
   ```
   - **构建镜像**：在包含 Dockerfile 的目录下运行命令 `docker build -t 镜像名称 .`。
   - **运行容器**：`docker run -p 8080:80 镜像名称`，将本地端口 8080 映射到容器的 80 端口。

### 5. Docker Compose
   Docker Compose 可以帮助你定义和管理多容器应用程序。
   
   **docker-compose.yml 示例**
   ```yaml
   version: '3'
   services:
     web:
       image: nginx
       ports:
         - "8080:80"
     db:
       image: mysql
       environment:
         MYSQL_ROOT_PASSWORD: example
   ```
   - **启动服务**：在 `docker-compose.yml` 文件所在目录运行 `docker-compose up`。
   - **停止服务**：`docker-compose down`

### 6. 常用 Docker 命令
   - **查看容器日志**：`docker logs 容器ID或名称`
   - **进入正在运行的容器**：`docker exec -it 容器ID或名称 bash`
   - **保存容器为镜像**：`docker commit 容器ID 镜像名称:标签`
   
### 7. 推送和拉取镜像
   - 登录 Docker Hub：`docker login`
   - **推送镜像**：`docker push 用户名/镜像名称`
   - **拉取镜像**：`docker pull 镜像名称`

学习和实践 Docker 命令，可以帮助你更好地理解和使用 Docker，优化应用程序的开发和部署流程。