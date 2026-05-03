# 局域网服务器公开到公网的方法

当只有局域网服务器可以访问公网服务器时，有两种主要方案：反向代理+SSH隧道，或内网穿透工具。

## 方法一：反向代理 + SSH 隧道

在局域网服务器和公网服务器之间创建 SSH 隧道，使公网服务器可以通过隧道访问局域网服务。

### 创建 SSH 反向隧道

在局域网服务器上执行：

```bash
ssh -R 公网端口:localhost:局域网端口 用户@公网服务器IP
```

示例（将本地 80 端口映射到公网 8080）：
```bash
ssh -R 8080:localhost:80 user@公网服务器IP
```

### 配置 Nginx 反向代理（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 方法二：内网穿透工具（推荐）

推荐使用 FRP、ngrok 或 NPS 等专业工具，更适合长期稳定使用。

### FRP 配置示例

**服务端 (frps.ini)：**
```ini
[common]
bind_port = 7000
```

**客户端 (frpc.ini)：**
```ini
[common]
server_addr = 公网服务器IP
server_port = 7000

[web]
type = http
local_port = 局域网服务端口
custom_domains = 公网服务器域名
```

两种方法都可以将局域网服务公开到公网。FRP 等内网穿透工具更适合长期使用，配置管理也更方便。
