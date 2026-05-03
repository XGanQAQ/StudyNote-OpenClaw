在C++中，`unordered_map` 是一种**哈希表**结构的关联容器，与 `map` 类似，主要用于存储键-值对，但 `unordered_map` **不保证元素的顺序**。由于使用哈希表，`unordered_map` 能提供平均为 \(O(1)\) 的查找、插入和删除效率，但其效率依赖于哈希函数和负载因子。`unordered_map` 位于 `<unordered_map>` 头文件中。

### 1. 基本操作

- **插入元素**：可以使用 `[]` 运算符或 `insert` 函数插入键值对。
    ```cpp
    unordered_map<string, int> umap;
    umap["apple"] = 3;         // 使用 [] 插入元素
    umap.insert({"banana", 5});  // 使用 insert 插入元素
    ```

- **访问元素**：使用 `[]` 运算符访问或修改指定键的值。如果键不存在，会自动插入该键，默认值为零初始化。
    ```cpp
    int value = umap["apple"];  // 获取键 "apple" 的值
    umap["apple"] = 4;          // 修改键 "apple" 的值
    ```

- **查找元素**：使用 `find` 方法查找指定键，返回指向该元素的迭代器。如果未找到，返回 `unordered_map::end`。
    ```cpp
    auto it = umap.find("banana");
    if (it != umap.end()) {
        cout << "Found banana with value: " << it->second << endl;
    }
    ```

- **删除元素**：可以使用 `erase` 方法按键或迭代器删除元素。
    ```cpp
    umap.erase("apple");  // 按键删除
    ```

- **`count`**：检查某个键是否存在。返回值为 `1`（存在）或 `0`（不存在）。
    ```cpp
    if (umap.count("banana")) {
        cout << "Banana exists in the unordered_map." << endl;
    }
    ```

- **`size`** 和 **`empty`**：获取元素数量和检查是否为空。
    ```cpp
    int n = umap.size();  // 获取 unordered_map 中的元素数量
    bool isEmpty = umap.empty();  // 判断 unordered_map 是否为空
    ```

### 2. 遍历 `unordered_map`

可以使用迭代器或 `range-based for` 循环遍历 `unordered_map`：

```cpp
for (auto it = umap.begin(); it != umap.end(); ++it) {
    cout << it->first << ": " << it->second << endl;
}

// 使用 range-based for 循环
for (const auto& pair : umap) {
    cout << pair.first << ": " << pair.second << endl;
}
```

### 3. 示例代码

以下是一个使用 `unordered_map` 的例子，实现了简单的词频统计：

```cpp
#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

using namespace std;

int main() {
    vector<string> words = {"apple", "banana", "apple", "orange", "banana", "apple"};
    unordered_map<string, int> wordCount;

    // 统计词频
    for (const string& word : words) {
        wordCount[word]++;  // 如果键已存在，则计数+1；否则创建键并初始化为1
    }

    // 输出词频统计结果
    for (const auto& pair : wordCount) {
        cout << pair.first << ": " << pair.second << endl;
    }

    return 0;
}
```

### 4. 注意事项

- **无序性**：`unordered_map` 不保证键值对的顺序，与插入顺序无关，遍历的顺序可能会因不同的哈希函数实现而不同。
- **时间复杂度**：`unordered_map` 的插入、查找和删除平均为 \(O(1)\)，但最坏情况下可能退化为 \(O(n)\)，例如当所有键发生哈希碰撞时。
- **键的唯一性**：`unordered_map` 中的键是唯一的，插入相同键会覆盖旧值。如果需要存储相同键的多个值，可以使用 `unordered_multimap`。
- **哈希函数**：默认使用 `std::hash` 计算哈希值。