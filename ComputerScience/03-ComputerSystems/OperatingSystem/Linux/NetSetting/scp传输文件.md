`scp`（Secure Copy Protocol）是用于在网络中安全地传输文件的一种方式，它利用SSH协议进行加密传输。以下是使用`scp`传输文件的一些基本操作方法：

### 1. 从本地机器传输文件到远程机器
```bash
scp /path/to/local/file username@remote_host:/path/to/remote/directory
```
- `/path/to/local/file`：本地文件的路径。
- `username`：远程机器的用户名。
- `remote_host`：远程机器的IP地址或主机名。
- `/path/to/remote/directory`：远程机器上目标目录的路径。

### 2. 从远程机器传输文件到本地机器
```bash
scp username@remote_host:/path/to/remote/file /path/to/local/directory
```
- `username@remote_host:/path/to/remote/file`：远程文件的路径。
- `/path/to/local/directory`：本地目标目录的路径。

### 3. 传输整个目录
使用`-r`选项可以递归地复制整个目录：
```bash
scp -r /path/to/local/directory username@remote_host:/path/to/remote/directory
```

### 4. 使用自定义端口进行连接
如果SSH服务器使用非默认端口（默认端口是22），可以使用`-P`选项指定端口号：
```bash
scp -P port_number /path/to/local/file username@remote_host:/path/to/remote/directory
```
- `port_number`：远程SSH服务器的端口号。

### 5. 传输文件并指定不同的文件名
你也可以在目标路径指定一个新的文件名：
```bash
scp /path/to/local/file username@remote_host:/path/to/remote/directory/new_filename
```

### 6. 使用SSH密钥进行认证
如果你的远程机器配置了SSH密钥认证而非密码认证，可以使用`-i`选项指定私钥：
```bash
scp -i /path/to/private_key /path/to/local/file username@remote_host:/path/to/remote/directory
```

### 示例：
假设你要将本地的`document.txt`文件上传到远程服务器的`/home/user/docs/`目录，并且使用默认端口22：
```bash
scp document.txt user@192.168.1.100:/home/user/docs/
```

如果有任何问题，随时告诉我！