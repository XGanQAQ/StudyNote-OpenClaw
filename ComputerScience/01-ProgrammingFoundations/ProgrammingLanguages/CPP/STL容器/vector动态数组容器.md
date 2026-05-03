C++ 的 `std::vector` 是一个动态数组容器，提供了灵活的内存管理和许多常用操作。以下是 `std::vector` 的一些常用方法和功能的总结：

### 1. 创建和初始化
- **构造函数**:
  ```cpp
  std::vector<int> vec;                 // 创建空的 vector
  std::vector<int> vec(10);             // 创建包含 10 个元素的 vector，默认初始化为 0
  std::vector<int> vec(10, 5);          // 创建包含 10 个元素，每个元素初始化为 5
  std::vector<int> vec = {1, 2, 3};     // 使用初始化列表创建 vector
  ```

### 2. 访问元素
- **`at()`**: 安全访问元素，越界时会抛出异常。
  ```cpp
  vec.at(0); // 访问第一个元素
  ```
- **`operator[]`**: 直接访问元素，不进行边界检查。
  ```cpp
  vec[0]; // 访问第一个元素
  ```
- **`front()`**: 返回第一个元素。
  ```cpp
  vec.front();
  ```
- **`back()`**: 返回最后一个元素。
  ```cpp
  vec.back();
  ```

### 3. 修改元素
- **`push_back()`**: 在末尾添加元素。
  ```cpp
  vec.push_back(4);
  ```
- **`pop_back()`**: 删除最后一个元素。
  ```cpp
  vec.pop_back();
  ```
- **`insert()`**: 在指定位置插入元素。
  ```cpp
  vec.insert(vec.begin() + 1, 10); // 在第二个位置插入 10
  res.insert(res.end(), leftRes.begin(), leftRes.end());//在数组的末尾连接上另一个数组
  
  ```
- **`erase()`**: 删除指定位置的元素。
  ```cpp
  vec.erase(vec.begin() + 1); // 删除第二个元素
  ```

### 4. 大小和容量
- **`size()`**: 返回当前元素的数量。
  ```cpp
  vec.size();
  ```
- **`capacity()`**: 返回当前分配的存储容量。
  ```cpp
  vec.capacity();
  ```
- **`resize()`**: 改变容器的大小，新增元素初始化为默认值。
  ```cpp
  vec.resize(15); // 调整大小为 15
  ```
- **`clear()`**: 清空容器中的所有元素。
  ```cpp
  vec.clear();
  ```

### 5. 其他方法
- **`empty()`**: 检查容器是否为空。
  ```cpp
  vec.empty(); // 返回 true 或 false
  ```
- **`swap()`**: 交换两个 vector 的内容。
  ```cpp
  std::vector<int> vec2 = {1, 2, 3};
  vec.swap(vec2);
  ```

### 6. 迭代器
- **`begin()`**: 返回指向第一个元素的迭代器。
- **`end()`**: 返回指向最后一个元素后一个位置的迭代器。
- **`rbegin()` / `rend()`**: 返回反向迭代器。

### 7. 例子
以下是一个使用 `std::vector` 的简单示例：

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3};

    vec.push_back(4); // 添加元素
    vec.insert(vec.begin() + 1, 5); // 在第二个位置插入 5

    for (int i : vec) {
        std::cout << i << " "; // 输出元素
    }

    std::cout << "\nSize: " << vec.size() << "\n";
    std::cout << "Capacity: " << vec.capacity() << "\n";

    vec.erase(vec.begin()); // 删除第一个元素
    vec.clear(); // 清空 vector

    return 0;
}
```

### 结论
`std::vector` 提供了灵活且高效的动态数组功能，是 C++ STL 中最常用的容器之一。掌握其常用方法有助于高效地处理数据。