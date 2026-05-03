
## 🧩 完整示例：`docker-compose.yml`

```yaml
version: "3.9" # Compose 文件版本（推荐使用3或以上版本）

#############################
# 🔹 定义网络（可选）
#############################
networks:
  my_network:               # 网络名称，可供多个服务共用
    driver: bridge          # bridge为默认网络模式，相当于本地虚拟局域网
    # driver: host          # （可选）使用主机网络，容器共享宿主机端口
    # driver: none          # （可选）无网络（通常用于安全隔离）

#############################
# 🔹 定义卷（数据持久化）
#############################
volumes:
  app_data:                 # 定义一个命名卷（Docker 管理）
  db_data:                  # 另一份命名卷，用于数据库存储

#############################
# 🔹 定义服务（核心部分）
#############################
services:
  ##############################################
  # 🟢 应用服务（示例：Web 应用）
  ##############################################
  web:
    image: nginx:latest               # 使用官方 Nginx 镜像（也可用 build 自定义）
    container_name: my_nginx          # 容器名称（可选）
    restart: always                   # 容器重启策略：always / unless-stopped / on-failure
    ports:
      - "80:80"                       # 映射宿主机80端口到容器80端口
      - "443:443"                     # HTTPS端口（如果配置证书）
    environment:                      # 环境变量（传递给容器内部）
      - NGINX_PORT=80
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro  # 本地配置文件映射到容器（只读）
      - app_data:/usr/share/nginx/html        # 使用命名卷存储网站内容
    depends_on:                      # 依赖关系，确保 db 启动后再启动 web
      - db
    networks:
      - my_network                   # 加入自定义网络，与其他容器通信

  ##############################################
  # 🟡 数据库服务（示例：PostgreSQL）
  ##############################################
  db:
    image: postgres:15               # PostgreSQL 官方镜像
    container_name: my_postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=admin          # 数据库用户名
      - POSTGRES_PASSWORD=secret     # 数据库密码
      - POSTGRES_DB=myapp            # 默认创建的数据库名
    volumes:
      - db_data:/var/lib/postgresql/data # 数据持久化目录
    ports:
      - "5432:5432"                  # 映射数据库端口
    networks:
      - my_network

  ##############################################
  # 🔵 应用后端（示例：Node.js）
  ##############################################
  backend:
    build:                           # 从本地Dockerfile构建镜像
      context: ./backend             # 指定Dockerfile所在目录
      dockerfile: Dockerfile
    container_name: my_backend
    restart: on-failure              # 启动失败时重启
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://admin:secret@db:5432/myapp
    volumes:
      - ./backend:/usr/src/app       # 映射源代码目录（方便热更新）
    working_dir: /usr/src/app        # 容器启动时的工作目录
    command: ["npm", "start"]        # 覆盖镜像默认启动命令
    depends_on:
      - db
    networks:
      - my_network
    ports:
      - "3000:3000"                  # 应用服务端口

#############################
# ✅ 文件结束
#############################
```

---

## 📘 配置项汇总与说明

|配置项|类型|说明|
|---|---|---|
|`version`|必填|docker-compose 文件规范版本|
|`services`|必填|定义容器服务（每个服务相当于一个容器）|
|`image`|字符串|指定使用的镜像|
|`build`|对象|从 Dockerfile 构建镜像（可自定义 context 和 dockerfile）|
|`container_name`|字符串|给容器命名（默认会自动生成）|
|`ports`|列表|端口映射 `宿主机:容器端口`|
|`environment`|列表或字典|设置环境变量|
|`volumes`|列表|数据卷或宿主机目录映射|
|`networks`|列表|指定加入的网络|
|`depends_on`|列表|设置容器启动顺序依赖|
|`restart`|字符串|重启策略|
|`command`|列表或字符串|覆盖镜像内的默认命令|
|`working_dir`|字符串|设置容器内的工作目录|
|`networks:`（顶级）|字典|定义可共享的网络（跨服务通信）|
|`volumes:`（顶级）|字典|定义命名卷（跨容器持久化数据）|

---

## 🚀 实用命令（配合 Compose 使用）

|命令|作用|
|---|---|
|`docker-compose up -d`|后台启动所有服务|
|`docker-compose down`|停止并移除容器、网络（保留卷）|
|`docker-compose down -v`|停止并删除卷（⚠️ 数据清空）|
|`docker-compose logs -f`|查看实时日志|
|`docker-compose restart <服务名>`|重启指定服务|
|`docker-compose exec <服务名> bash`|进入容器终端|
|`docker-compose ps`|查看当前服务状态|

---

## 🧠 总结

要**全面理解 Docker Compose**，你应该掌握以下五大核心概念：

|分类|概念|作用|
|---|---|---|
|🧱 核心结构|service、image、container|Compose 管理的对象|
|💾 存储|volume、bind mount|数据持久化与共享|
|🌐 网络|network、bridge|容器间通信与隔离|
|⚙️ 环境|environment、command、depends_on|控制启动逻辑|
|🧩 管理|restart、logs、up/down|服务生命周期管理|
