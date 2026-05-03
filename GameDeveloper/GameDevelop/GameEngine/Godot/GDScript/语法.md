Godot 使用的 GDScript 是一种专为游戏开发设计的脚本语言，语法简洁易学，类似 Python。以下是 GDScript 的一些基础语法规则和常用功能：

### 1. **注释**
   - 单行注释：以 `#` 开头。
     ```gdscript
     # 这是一个单行注释
     ```
   - 多行注释：使用 `"""` 或 `'''`。
     ```gdscript
     """
     这是一个多行注释
     可以用于注释多行内容
     """
     ```

### 2. **变量声明与赋值**
   GDScript 是动态类型语言，不需要显式声明类型。
   ```gdscript
   var health = 100  # 整数
   var player_name = "Hero"  # 字符串
   var is_alive = true  # 布尔值
   var position = Vector2(10, 20)  # 向量
   ```

   - **常量**：使用 `const` 声明常量。
     ```gdscript
     const MAX_HEALTH = 200
     ```

### 3. **函数**
   定义函数使用 `func` 关键字，函数参数可以有默认值。
   ```gdscript
   func move_player(direction, speed=5):
       position += direction * speed
   ```

   **返回值**：函数默认返回 `null`，但可以使用 `return` 语句显式返回值。
   ```gdscript
   func add(a, b):
       return a + b
   ```

### 4. **条件语句**
   GDScript 使用常见的条件语句，结构和 Python 相似。
   ```gdscript
   if health <= 0:
       print("Player is dead")
   elif health > 0 and health <= 50:
       print("Player is hurt")
   else:
       print("Player is healthy")
   ```

### 5. **循环**
   支持 `for` 循环和 `while` 循环。
   - **for 循环**：
     ```gdscript
     for i in range(10):  # 从 0 到 9
         print(i)
     ```
   - **while 循环**：
     ```gdscript
     var i = 0
     while i < 10:
         print(i)
         i += 1
     ```

### 6. **数组和字典**
   - **数组**：数组是一个有序的集合，可以包含任何类型的元素。
     ```gdscript
     var numbers = [1, 2, 3, 4, 5]
     var strings = ["hello", "world"]
     numbers.append(6)  # 向数组添加元素
     print(numbers[0])  # 访问第一个元素
     ```
   - **字典**：字典是键值对集合。
     ```gdscript
     var player = {"name": "Hero", "health": 100}
     print(player["name"])  # 访问键值
     player["health"] = 80  # 修改值
     ```

### 7. **类和继承**
   GDScript 支持面向对象编程，使用 `class_name` 来声明类，继承用 `extends`。
   ```gdscript
   class_name Player  # 声明一个名为 Player 的类

   var health = 100

   func take_damage(damage):
       health -= damage
       if health <= 0:
           die()

   func die():
       print("Player died")
   ```

   **继承**：
   ```gdscript
   class Enemy extends Player:
       var damage = 10

       func attack():
           take_damage(damage)
   ```

### 8. **信号（Signals）**
   GDScript 支持信号，允许节点之间进行解耦的通信。
   - **声明信号**：
     ```gdscript
     signal health_changed
     ```
   - **发射信号**：
     ```gdscript
     emit_signal("health_changed", health)
     ```
   - **连接信号**：
     ```gdscript
     $Player.connect("health_changed", self, "_on_health_changed")
     ```

### 9. **节点和场景**
   GDScript 主要与 Godot 中的节点进行交互，通常通过 `$` 符号引用节点。
   ```gdscript
   var player = $Player  # 获取当前节点下的 Player 子节点
   player.position = Vector2(100, 200)  # 修改 Player 的位置
   ```

### 10. **异常处理**
   GDScript 支持基本的错误处理，可以使用 `try` 和 `except`。
   ```gdscript
   try:
       var result = 10 / 0  # 可能引发除零错误
   except Error as e:
       print("Error:", e)
   ```

### 11. **迭代器与生成器**
   GDScript 允许使用 `yield` 关键字来暂停函数，常用于异步处理。
   ```gdscript
   func example():
       yield(get_tree().create_timer(2), "timeout")  # 等待2秒
       print("2 seconds passed")
   ```

### 12. **枚举**
   可以使用 `enum` 声明一个枚举类型：
   ```gdscript
   enum State { IDLE, RUNNING, JUMPING }

   var current_state = State.IDLE
   ```

### 13. **运算符**
   支持常见的算术运算符、逻辑运算符、位运算符等。
   - 算术运算符：`+`, `-`, `*`, `/`, `%`, `**` (幂运算)
   - 逻辑运算符：`and`, `or`, `not`
   - 位运算符：`&`, `|`, `^`, `<<`, `>>`

### 14. **类型注解**
   可以使用类型注解来明确变量、函数参数和返回值的类型。
   ```gdscript
   var health: int = 100
   func add(a: int, b: int) -> int:
       return a + b
   ```

### 15. **预处理器指令**
   GDScript 支持一些预处理器指令，如 `@export` 和 `@tool` 等。
   - `@export` 用于将变量暴露给 Godot 编辑器。
     ```gdscript
     @export var speed = 10
     ```

### 总结
GDScript 的语法非常简洁且接近 Python，适合快速开发和脚本化游戏逻辑。它的内置功能强大且与 Godot 引擎紧密集成，使得游戏开发过程更加高效。