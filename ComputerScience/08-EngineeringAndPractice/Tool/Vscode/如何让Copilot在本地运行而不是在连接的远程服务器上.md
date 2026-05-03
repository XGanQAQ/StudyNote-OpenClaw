
打开Settings
![[Pasted image 20250524230802.png]]
找到这个链接打开json配置
![[Pasted image 20250524230837.png]]
你可能会看到一堆配置，然后在"github.copilot.advanced":{}中加入如下字段，结果如图。
```
"github.copilot.enable": {
  "*": true,
  "github.dev": true,
  "codespaces": true,
  "vscode-remote": false
}
```

这个配置的含义是：

| 位置                           | 是否启用 |
| ---------------------------- | ---- |
| 本地 VSCode (`*`)              | ✅ 开启 |
| Remote-SSH (`vscode-remote`) | ❌ 关闭 |
| GitHub Codespaces 等          | ✅ 开启 |
如果没有效果，记得重启 VSCode。

我是成功了