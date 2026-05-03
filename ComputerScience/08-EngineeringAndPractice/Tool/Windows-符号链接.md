
在 Windows 里你要做的是“符号链接（Symbolic Link）”，本质就是：**在A目录放一个“假文件”，但它实际指向B目录的真实文件**。

```
mklink <链接(假文件)> <目标(真实文件)>
```

```powershell
New-Item -ItemType SymbolicLink `
  -Path "C:\Dev\Project\development-plugin-for-avalonia\.github\plugin\plugin.json" `
  -Target "C:\Dev\Project\development-plugin-for-avalonia\plugin.json"
```

# ⚠️ 使用前检查（很关键）

## 1️⃣ 确保目标存在

```text
C:\Dev\Project\development-plugin-for-avalonia\plugin.json
```

---

## 2️⃣ 确保链接位置不存在同名文件

如果已经存在：

```powershell
Remove-Item "C:\Dev\Project\development-plugin-for-avalonia\.github\plugin\plugin.json"
```

---

## 3️⃣ 目录必须存在

```text
.github\plugin\
```

不存在就先创建：

```powershell
New-Item -ItemType Directory -Path "C:\Dev\Project\development-plugin-for-avalonia\.github\plugin"
```

---
