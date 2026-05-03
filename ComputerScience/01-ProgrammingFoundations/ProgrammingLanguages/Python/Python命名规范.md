在 Python 中，遵循命名规范是编写可读性强、易于维护的代码的重要部分。以下是一些常见的 Python 命名规范：

### 1. **变量和函数命名**
   - **小写字母和下划线**：使用小写字母和下划线（snake_case）来命名变量和函数。例如：
     ```python
     def calculate_area(radius):
         return 3.14 * radius ** 2
     
     total_price = 100
     ```
   - **避免使用单个字符**：除非在循环或临时使用的情况下，尽量避免使用单个字符（如 `x`, `y`, `z`），而是选择具有描述性的名称。

### 2. **类命名**
   - **驼峰命名法**：类名应该使用大写字母开头的驼峰命名法（CamelCase），每个单词的首字母都大写。例如：
     ```python
     class Circle:
         def __init__(self, radius):
             self.radius = radius
     ```

### 3. **常量命名**
   - **全大写字母和下划线**：常量名通常使用全大写字母和下划线（UPPER_CASE_WITH_UNDERSCORES）来表示。例如：
     ```python
     PI = 3.14159
     MAX_CONNECTIONS = 10
     ```

### 4. **模块和包命名**
   - **小写字母**：模块名和包名应使用小写字母，并且可以使用下划线分隔单词（但不推荐使用下划线）。例如：
     ```python
     # 模块名
     import my_module
     
     # 包名
     import mypackage
     ```

### 5. **私有变量和函数**
   - **前缀下划线**：使用单个下划线（_）作为前缀来表示私有变量和函数。例如：
     ```python
     class MyClass:
         def __init__(self):
             self._private_var = 42
         
         def _private_method(self):
             return "This is a private method."
     ```
   - **双下划线**：使用双下划线（__）可以触发名称修饰，表示变量是类的私有，防止子类覆盖。例如：
     ```python
     class MyClass:
         def __init__(self):
             self.__private_var = 42
     ```

### 6. **避免保留字**
   - 不要使用 Python 的保留字（如 `if`, `else`, `for`, `while`, `def`, `class` 等）作为变量名或函数名。

### 7. **长度适中**
   - 尽量使变量和函数名具有描述性，但又不要过长。名称应能够清晰表达其功能或用途。

### 8. **使用可读性**
   - 命名时要确保可读性，即使是在复杂的代码中，其他人也能快速理解变量或函数的含义。

### 9. **遵循 PEP 8 标准**
   - Python 官方推荐遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范，该文档详细描述了 Python 编码风格，包括命名约定和其他编程习惯。

### 示例
以下是一个示例，展示了如何在 Python 中应用这些命名规范：

```python
class Circle:
    PI = 3.14159  # 常量
    
    def __init__(self, radius):
        self._radius = radius  # 私有变量
    
    def calculate_area(self):  # 函数
        return Circle.PI * (self._radius ** 2)  # 使用常量
    
    def _private_method(self):  # 私有方法
        return "This is a private method."
```

### 总结
遵循 Python 的命名规范能够提高代码的可读性和可维护性，使得团队协作和代码审核更为顺畅。通过一致的命名约定，其他开发者（或未来的自己）能够更轻松地理解和使用代码。