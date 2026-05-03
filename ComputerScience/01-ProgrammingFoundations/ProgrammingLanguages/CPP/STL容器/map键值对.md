在C++中，`map` 是一个常用的**关联容器**，可以存储键-值对（即 `key-value` 对）。`map` 默认按键的**升序**进行排序，支持高效的查找、插入、删除等操作。`map` 类位于 `<map>` 头文件中。以下是 `map` 类的常用方法：

### 1. 基本操作

- **插入元素**：可以使用 `[]` 运算符或 `insert` 函数插入键值对。
    ```cpp
    map<string, int> m;
    m["apple"] = 3;  // 使用 [] 插入元素，键为 "apple"，值为 3
    m.insert({"banana", 5});  // 使用 insert 插入元素
    ```

- **访问元素**：使用 `[]` 运算符访问或修改指定键的值。
    ```cpp
    int value = m["apple"];  // 获取键 "apple" 的值
    m["apple"] = 4;          // 修改键 "apple" 的值
    ```

- **查找元素**：使用 `find` 方法查找指定键，返回一个迭代器指向该元素。如果未找到，返回 `map::end`。
    ```cpp
    auto it = m.find("banana");
    if (it != m.end()) {
        cout << "Found banana with value: " << it->second << endl;
    }
    ```

- **删除元素**：可以使用 `erase` 方法按键或迭代器删除元素。
    ```cpp
    m.erase("apple");  // 按键删除
    ```

- **`count`**：检查某个键是否存在，返回值为 `1`（存在）或 `0`（不存在）。
    ```cpp
    if (m.count("banana")) {
        cout << "Banana exists in the map." << endl;
    }
    ```

- **`size`** 和 **`empty`**：获取元素数量和检查是否为空。
    ```cpp
    int n = m.size();  // 获取 map 中的元素数量
    bool isEmpty = m.empty();  // 判断 map 是否为空
    ```

### 2. 遍历 `map`

可以使用迭代器遍历 `map`，或使用 `range-based for` 循环：

```cpp
for (auto it = m.begin(); it != m.end(); ++it) {
    cout << it->first << ": " << it->second << endl;
}

// 使用 range-based for 循环
for (const auto& pair : m) {
    cout << pair.first << ": " << pair.second << endl;
}
```

- `pair.first`：键
- `pair.second`：值


### 3. 示例代码

以下是一个使用 `map` 的例子，实现了一个简单的词频统计：

```cpp
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

int main() {
    vector<string> words = {"apple", "banana", "apple", "orange", "banana", "apple"};
    map<string, int> wordCount;

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
- **按键排序**：`map` 按键自动排序，默认按升序。如果需要按自定义规则排序，可以使用 `std::less` 等比较函数。
- **键的唯一性**：`map` 中的键是唯一的，插入相同键时会覆盖旧值。如果需要存储相同键的多个值，可以使用 `multimap`。
- **时间复杂度**：`map` 是基于平衡二叉树（通常是红黑树）实现的，插入、查找、删除的时间复杂度为 \(O(\log n)\)。