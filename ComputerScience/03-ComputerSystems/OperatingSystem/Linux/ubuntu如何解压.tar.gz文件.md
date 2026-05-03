在 Ubuntu 中，你可以使用 `tar` 命令来解压 `.tar.gz` 文件。下面是常用的命令：

### 解压 `.tar.gz` 文件的命令：
```bash
tar -xzvf filename.tar.gz
```

### 参数解释：
- `x`：表示解压（extract）。
- `z`：表示通过 gzip 解压（因为文件是 `.gz` 格式）。
- `v`：表示显示详细输出（verbose），解压过程中会显示文件列表。
- `f`：表示指定文件名，`filename.tar.gz` 是你要解压的文件名。

### 示例：
假设你的文件名是 `example.tar.gz`，你可以这样解压：
```bash
tar -xzvf example.tar.gz
```

解压后，文件会被提取到当前目录下。

### 解压到指定目录：
如果你想将文件解压到指定的目录，可以使用 `-C` 参数：
```bash
tar -xzvf example.tar.gz -C /path/to/directory
```
这将把 `example.tar.gz` 解压到 `/path/to/directory` 目录。

希望这些说明对你有所帮助！