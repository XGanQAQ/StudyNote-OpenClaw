# Python列表推导式原理与语法

列表推导式(List Comprehension)是Python中一种简洁高效创建列表的方式，它比传统的for循环加append的方式更加优雅和高效。

## 基本语法

```python
[expression for item in iterable]
```

这相当于：

```python
result = []
for item in iterable:
    result.append(expression)
```

## 完整语法形式

```python
[expression for item in iterable if condition]
```

这相当于：

```python
result = []
for item in iterable:
    if condition:
        result.append(expression)
```

## 多层循环推导式

```python
[expression for item1 in iterable1 for item2 in iterable2]
```

相当于：

```python
result = []
for item1 in iterable1:
    for item2 in iterable2:
        result.append(expression)
```

## 实际示例

1. **基本示例**：
```python
squares = [x**2 for x in range(10)]
# 结果: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

2. **带条件的推导式**：
```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
# 结果: [0, 4, 16, 36, 64]
```

3. **多层循环**：
```python
pairs = [(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
# 结果: [(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
```

4. **嵌套推导式**：
```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flatten = [num for row in matrix for num in row]
# 结果: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## 性能考虑

列表推导式通常比等效的for循环更快，因为：
1. 解释器可以优化推导式的执行
2. 减少了方法调用（如append()）的开销

## 其他推导式

Python还支持类似的推导式语法：

1. **字典推导式**：
```python
{x: x**2 for x in (2, 4, 6)}
# 结果: {2: 4, 4: 16, 6: 36}
```

2. **集合推导式**：
```python
{x for x in 'abracadabra' if x not in 'abc'}
# 结果: {'d', 'r'}
```

3. **生成器表达式**（使用圆括号）：
```python
(x**2 for x in range(10))
# 返回一个生成器对象，惰性求值
```

列表推导式是Python中非常强大且常用的特性，合理使用可以使代码更加简洁高效。