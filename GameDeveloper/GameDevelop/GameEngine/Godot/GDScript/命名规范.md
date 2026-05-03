在 Godot 中使用 GDScript 时，遵循良好的命名规范可以帮助代码保持清晰和易读。Godot 官方建议的 GDScript 命名规范如下：

### 1. **类名**
- 类名使用 **帕斯卡命名法**（PascalCase）。
- 每个单词的首字母大写，其他字母小写，单词之间不使用分隔符。

示例：
```gdscript
class_name PlayerController
```

### 2. **变量名**
- 变量名使用 **蛇形命名法**（snake_case）。
- 全部字母小写，单词之间使用下划线分隔。

示例：
```gdscript
var player_health = 100
```

### 3. **常量**
- 常量名使用 **全大写字母**，并且单词之间使用下划线分隔。

示例：
```gdscript
const MAX_HEALTH = 100
const PI_VALUE = 3.14159
```

### 4. **函数名**
- 函数名使用 **蛇形命名法**（snake_case）。
- 全部字母小写，单词之间使用下划线分隔。

示例：
```gdscript
func move_player(delta):
    pass
```

### 5. **信号名**
- 信号名使用 **蛇形命名法**（snake_case）。
- 和变量名、函数名保持一致。

示例：
```gdscript
signal health_changed
```

### 6. **文件和资源命名**
- 脚本文件名也使用 **蛇形命名法**，并尽量与类名对应。
- 场景文件、纹理、声音等资源文件的命名也应保持简洁，使用蛇形命名法。

示例：
```plaintext
player_controller.gd
main_menu.tscn
player_texture.png
```

### 7. **缩进和空格**
- GDScript 使用 **4 个空格** 作为缩进，不使用 Tab。
- 不要在行尾留多余的空格。

### 8. **注释**
- 单行注释使用 `#`。
- 多行注释可以使用多行 `#` 或者 `""" """`。

示例：
```gdscript
# This is a single-line comment.

"""
This is a multi-line comment.
It can span multiple lines.
"""
```

### 9. **布尔变量**
- 布尔变量名应以 `is_` 或 `has_` 开头，明确表达状态。

示例：
```gdscript
var is_player_alive = true
var has_key = false
```

### 10. **回调函数**
- Godot 引擎中的回调函数（如 `_ready()`、`_process()` 等）保持下划线开头，这些是引擎的内置约定。

示例：
```gdscript
func _ready():
    pass

func _process(delta):
    pass
```

### 总结
GDScript 的命名规范强调统一性和可读性，通过遵循这些约定，可以让代码在团队协作和长期维护时更加清晰和易于理解。