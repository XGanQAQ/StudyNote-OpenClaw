在 C# 中编写算法题时，有一些非常常用且高效的函数、类和方法。掌握它们可以大大简化你的代码，并提高解题效率。以下是一些最常用的：

### 1. `System.Math` 类

这个类提供了许多用于数学运算的静态方法，是算法题中最常见的一类工具。

- **`Math.Min(a, b)` 和 `Math.Max(a, b)`**: 找两个数中的较小值或较大值。
    
- **`Math.Abs(x)`**: 绝对值。
    
- **`Math.Pow(x, y)`**: 计算 `x` 的 `y` 次方。
    
- **`Math.Sqrt(x)`**: 平方根。
    
- **`Math.Floor(d)` 和 `Math.Ceiling(d)`**: 向下或向上取整。
    

### 2. 数组和列表

C# 中处理集合数据时，`Array` 和 `List<T>` 是最基本的工具。

- **数组 (`T[]`)**:
    
    - `array.Length`: 获取数组长度。
        
    - `Array.Sort(array)`: 对数组进行升序排序。
        
    - `Array.Reverse(array)`: 反转数组中的元素顺序。
        
    - `Array.BinarySearch(array, value)`: 在已排序的数组中查找指定元素，返回其索引。
        
- **列表 (`List<T>`)**:
    
    - `list.Count`: 获取列表中的元素数量。
        
    - `list.Add(item)`: 在列表末尾添加元素。
        
    - `list.Remove(item)` / `list.RemoveAt(index)`: 移除元素。
        
    - `list.Sort()`: 对列表进行排序。
        
    - `list.ToArray()`: 将列表转换为数组。
        

### 3. `System.Linq` 命名空间

**LINQ (Language Integrated Query)** 是 C# 中一个强大的功能，可以让你以非常简洁的方式操作集合。许多算法题都可以用 LINQ 变得更简单。

- **`array.Sum()`**: 计算集合中所有元素的总和。
    
- **`array.Min()` / `array.Max()`**: 找到集合中的最小值或最大值。
    
- **`array.Average()`**: 计算平均值。
    
- **`array.Count()`**: 计算元素数量。
    
- **`array.Distinct()`**: 返回一个去重后的新集合。
    
- **`array.OrderBy(x => x.Property)` / `array.OrderByDescending(...)`**: 按指定属性对集合进行排序。
    
- **`array.Where(x => condition)`**: 根据条件筛选元素。
    

### 4. 字符串 (`string`)

字符串在许多算法题（特别是涉及文本处理的）中非常重要。

- **`str.Length`**: 获取字符串长度。
    
- **`str.Substring(startIndex, length)`**: 获取子字符串。
    
- **`str.Split(char)`**: 根据分隔符将字符串分割成子字符串数组。
    
- **`str.Replace(oldChar, newChar)`**: 替换字符串中的字符。
    
- **`str.ToCharArray()`**: 将字符串转换为字符数组，方便操作。
    
- **`str.Contains(substring)`**: 检查字符串是否包含子字符串。
    

### 5. 其他常用数据结构和方法

- **栈 (`Stack<T>`) 和队列 (`Queue<T>`)**:
    
    - **栈**: `Push()`, `Pop()`, `Peek()`。常用于回溯、深度优先搜索 (DFS) 等问题。
        
    - **队列**: `Enqueue()`, `Dequeue()`, `Peek()`。常用于广度优先搜索 (BFS) 等问题。
        
- **哈希集合 (`HashSet<T>`) 和字典 (`Dictionary<K, V>`)**:
    
    - **`HashSet`**: 用于高效地存储唯一元素，常用于去重和快速查找。`hashSet.Add()`, `hashSet.Contains()`.
        
    - **`Dictionary`**: 键值对存储，常用于统计频率或建立映射关系。`dictionary[key]`, `dictionary.ContainsKey()`, `dictionary.Add()`.
        

### 示例：如何结合使用这些工具

假设你要解决一个问题：统计一个整型数组中每个数字出现的次数。

```csharp
using System;
using System.Collections.Generic;

public class Solution {
    public Dictionary<int, int> CountFrequency(int[] numbers) {
        Dictionary<int, int> frequencyMap = new Dictionary<int, int>();

        foreach (int num in numbers) {
            // 使用 TryGetValue 避免重复检查键是否存在
            if (frequencyMap.ContainsKey(num)) {
                frequencyMap[num]++;
            } else {
                frequencyMap[num] = 1;
            }

            // 或者更简洁的方式（C# 7.0+）
            // frequencyMap.TryGetValue(num, out int count);
            // frequencyMap[num] = count + 1;
        }

        return frequencyMap;
    }
}
```

这段代码使用了 **`Dictionary`** 这个数据结构，能够以 `O(1)` 的平均时间复杂度完成查找、插入和更新操作，非常适合这类计数问题。

在刷题过程中，多思考如何利用这些现成的数据结构和方法，可以帮助你写出更简洁、更高效的代码。