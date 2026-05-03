# Python 的真值测试规则

在 Python 中，任何对象都可以进行真值测试（即在布尔上下文中被评估为 `True` 或 `False`）。以下是 Python 的真值测试规则：

## 基本规则

1. 以下对象被视为 `False`：
   - `None`
   - `False`
   - 数值类型的零：`0`, `0.0`, `0j`
   - 空序列：`""`, `()`, `[]`
   - 空映射：`{}`
   - 用户定义类的实例，如果该类定义了 `__bool__()` 或 `__len__()` 方法并且返回 `False` 或 `0`

2. 所有其他对象都被视为 `True`

## 示例

```python
# 被视为 False 的情况
print(bool(None))      # False
print(bool(False))     # False
print(bool(0))         # False
print(bool(0.0))       # False
print(bool(0j))        # False
print(bool(""))        # False
print(bool([]))        # False
print(bool(()))        # False
print(bool({}))        # False

# 被视为 True 的情况
print(bool(1))         # True
print(bool(-1))        # True
print(bool(0.1))       # True
print(bool(" "))       # True
print(bool([False]))   # True
print(bool((None,)))   # True
print(bool({"a": 1}))  # True
```

## 自定义类的真值测试

对于用户定义的类，可以通过以下方式控制其实例的真值：

1. 定义 `__bool__()` 方法，它应该返回 `True` 或 `False`
2. 如果没有定义 `__bool__()`，Python 会检查 `__len__()` 方法，如果长度为 0 则为 `False`，否则为 `True`
3. 如果两者都未定义，则实例总是被视为 `True`

```python
class MyClass:
    def __init__(self, value):
        self.value = value
    
    def __bool__(self):
        return bool(self.value)

print(bool(MyClass(0)))   # False
print(bool(MyClass(1)))   # True

class MyList:
    def __init__(self, items):
        self.items = items
    
    def __len__(self):
        return len(self.items)

print(bool(MyList([])))   # False
print(bool(MyList([1])))  # True
```

## 实际应用

真值测试常用于条件语句中：

```python
value = input("请输入内容: ")
if value:  # 等价于 if value != ""
    print("你输入了:", value)
else:
    print("你没有输入任何内容")
```

理解 Python 的真值测试规则有助于编写更简洁、更 Pythonic 的代码。