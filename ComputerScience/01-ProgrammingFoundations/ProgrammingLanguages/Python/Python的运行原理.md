运行一个 `.py` 文件（Python代码）很简单，具体步骤如下：

### 1. **确保你安装了Python解释器**
首先，要确保你已经在电脑上安装了Python。如果你还没有安装，可以从[Python官网](https://www.python.org/downloads/)下载并安装Python。安装时请确保勾选了“Add Python to PATH”选项，这样你可以在终端中直接运行`python`命令。

### 2. **通过命令行运行.py文件**
一旦你有了Python解释器，就可以通过命令行（终端）运行你的Python脚本。

#### 2.1 **打开终端**
- 在Windows上，打开命令提示符（Command Prompt）或PowerShell。
- 在Mac或Linux上，打开Terminal。

#### 2.2 **导航到你的文件所在目录**
使用`cd`命令（Change Directory）进入存放`.py`文件的目录。例如，如果你的文件存放在`C:\myfolder`中（Windows）或`/home/user/myfolder`（Linux/Mac），你可以输入：

Windows:
```bash
cd C:\myfolder
```

Linux/Mac:
```bash
cd /home/user/myfolder
```

#### 2.3 **运行Python脚本**
在终端中输入以下命令来运行你的Python脚本：

- 如果你安装的是Python 3.x（大部分情况是这样），使用`python3`：
  ```bash
  python3 myscript.py
  ```

- 如果你只安装了Python 3，或者`python`指向Python 3.x，可以直接用`python`：
  ```bash
  python myscript.py
  ```

- 如果你在Windows系统中使用`python`，也有可能是指向Python 2.x版本。此时可以用`python3`来运行。

#### 2.4 **查看运行结果**
如果一切正常，命令行会显示你的程序输出。如果有错误，它会在终端中显示错误信息，你可以根据这些信息修改代码。

### 3. **通过集成开发环境（IDE）运行**
如果你不想通过命令行手动运行Python脚本，还可以使用一些集成开发环境（IDE）来运行代码，比如：

- **PyCharm**：一个功能强大的Python IDE，提供调试、测试和代码补全等功能。
- **VS Code**：一个轻量的编辑器，通过安装Python插件，可以支持Python开发和调试。
- **Jupyter Notebook**：用于交互式编程和数据分析的环境。

在IDE中，通常只需要点击“运行”按钮或者使用快捷键（如`Shift + F10`）来执行Python代码。

### 4. **运行.py文件的其他方式**
#### 4.1 **通过双击运行（仅限Windows）**
在Windows中，如果你已经将Python正确安装，并将Python添加到环境变量中，你可以通过双击`.py`文件来运行程序。但这种方式不适合调试，因为你不能看到错误信息。

#### 4.2 **通过文本编辑器的插件或集成功能**
一些文本编辑器（如Sublime Text、Atom等）也可以通过插件支持直接运行Python脚本，但配置起来稍微麻烦一点。

### 总结
最常用和最简单的方式是使用终端命令运行`python myscript.py`，这样你可以看到程序的输出和错误信息。如果你更喜欢图形界面，可以使用IDE来运行代码。