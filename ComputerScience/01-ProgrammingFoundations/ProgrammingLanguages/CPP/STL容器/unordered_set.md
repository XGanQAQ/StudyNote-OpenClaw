# unordered_set 无序集合
***set的意思为集合***  
表示一个不包含重复元素的集合，遵循集合论的基本原则。  
`unordered_set` 是 C++ 标准库中的一个关联容器，用于存储唯一元素。  
与 `set` 不同，`unordered_set` 使用哈希表来实现，提供了高效的查找和插入操作。  
以下是 `unordered_set` 的常用方法和属性：

### 常用方法

1. **插入元素**
   - `insert(const T& value)`: 将元素 `value` 插入到集合中。如果元素已经存在，则不插入。
   - `insert(InputIterator first, InputIterator last)`: 插入范围 `[first, last)` 中的所有元素。

   ```cpp
   std::unordered_set<int> mySet;
   mySet.insert(1);
   mySet.insert(2);
   mySet.insert(3);
   ```

2. **删除元素**
   - `erase(const T& value)`: 删除值为 `value` 的元素。
   - `erase(InputIterator first, InputIterator last)`: 删除范围 `[first, last)` 中的所有元素。
   - `erase(iterator position)`: 删除迭代器所指向的元素。

   ```cpp
   mySet.erase(2); // 删除值为 2 的元素
   ```

3. **查找元素**
   - `find(const T& value)`: 返回一个迭代器，指向值为 `value` 的元素，如果未找到，则返回 `end()`。
   - `count(const T& value)`: 返回值为 `value` 的元素个数（在 `unordered_set` 中为 0 或 1）。

   ```cpp
   auto it = mySet.find(1);
   if (it != mySet.end()) {
       // 找到元素 1
   }
   ```

4. **大小和容量**
   - `size()`: 返回集合中元素的个数。
   - `empty()`: 检查集合是否为空，返回布尔值。
   - `max_size()`: 返回集合能够容纳的最大元素数量（理论上）。

   ```cpp
   size_t setSize = mySet.size();
   bool isEmpty = mySet.empty();
   ```

5. **清空集合**
   - `clear()`: 删除集合中的所有元素。

   ```cpp
   mySet.clear(); // 清空集合
   ```

6. **迭代器**
   - `begin()`: 返回指向集合第一个元素的迭代器。
   - `end()`: 返回指向集合最后一个元素之后的位置的迭代器。

   ```cpp
   for (const auto& value : mySet) {
       std::cout << value << " ";
   }
   ```

7. **哈希函数和比较函数**
   - `hash_function()`: 返回用于计算元素哈希值的哈希函数。
   - `key_eq()`: 返回用于比较元素的函数。

   ```cpp
   auto hashFunc = mySet.hash_function();
   ```

### 属性

- **唯一性**: `unordered_set` 中的每个元素都是唯一的，不能重复。
- **无序性**: 元素不按照任何特定顺序存储，遍历时的顺序是不可预测的。
- **高效查找**: 插入、删除和查找的平均时间复杂度为 O(1)，最坏情况下为 O(n)（哈希冲突）。
- **动态扩展**: 当元素数量超过桶的容量时，`unordered_set` 会自动扩展以适应更多元素。

### 示例代码
以下是一个使用 `unordered_set` 的简单示例：
```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> mySet;

    // 插入元素
    mySet.insert(1);
    mySet.insert(2);
    mySet.insert(3);
    mySet.insert(2); // 不会插入重复元素

    // 查找元素
    if (mySet.find(3) != mySet.end()) {
        std::cout << "Found 3 in the set." << std::endl;
    }

    // 输出所有元素
    std::cout << "Elements in the unordered_set: ";
    for (const auto& value : mySet) {
        std::cout << value << " ";
    }
    std::cout << std::endl;

    // 删除元素
    mySet.erase(2);

    // 输出集合大小
    std::cout << "Size after erasing 2: " << mySet.size() << std::endl;

    return 0;
}
```

### 总结
`unordered_set` 提供了高效的元素查找和操作方法，适用于需要存储唯一元素但不关心元素顺序的场景。通过其提供的各种方法，开发者可以方便地管理和操作集合中的元素。