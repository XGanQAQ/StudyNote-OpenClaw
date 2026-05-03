在C++中，`queue` 是一种**先进先出 (FIFO)** 数据结构，适合用于按顺序处理数据的情景，例如任务调度、宽度优先搜索 (BFS) 等。`queue` 类位于 `<queue>` 头文件中。以下是 `queue` 类的常用方法：

### 1. 基本操作

- **`push`**：将元素添加到队列的末尾。
    ```cpp
    queue<int> q;
    q.push(10);  // 将 10 添加到队列末尾
    q.push(20);  // 将 20 添加到队列末尾
    ```

- **`pop`**：移除队列的第一个元素（即队首元素）。注意，`pop` 不会返回被删除的元素。
    ```cpp
    q.pop();  // 删除队首元素
    ```

- **`front`**：返回队首元素的引用，可以用于读取或修改队首元素。
    ```cpp
    int x = q.front();  // 获取队首元素
    q.front() = 15;     // 修改队首元素的值
    ```

- **`back`**：返回队尾元素的引用，可以用于读取或修改队尾元素。
    ```cpp
    int y = q.back();  // 获取队尾元素
    q.back() = 25;     // 修改队尾元素的值
    ```

- **`empty`**：检查队列是否为空。如果队列为空，则返回 `true`；否则返回 `false`。
    ```cpp
    if (q.empty()) {
        cout << "Queue is empty!" << endl;
    }
    ```

- **`size`**：返回队列中元素的个数。
    ```cpp
    int n = q.size();  // 获取队列中元素数量
    ```

### 2. 示例代码

以下是一个使用 `queue` 的例子，实现了一个简单的任务处理模拟：

```cpp
#include <iostream>
#include <queue>

using namespace std;

int main() {
    queue<string> tasks;
    
    // 添加任务
    tasks.push("Task 1: Write report");
    tasks.push("Task 2: Fix bug");
    tasks.push("Task 3: Review code");

    // 处理任务
    while (!tasks.empty()) {
        cout << "Processing " << tasks.front() << endl;  // 获取当前任务
        tasks.pop();  // 完成后移除当前任务
    }

    return 0;
}
```

### 3. 注意事项
- **无随机访问**：`queue` 不支持随机访问（如使用索引 `[]`），只能访问队首或队尾元素。
- **删除元素前应检查是否为空**：调用 `pop`、`front` 或 `back` 前应先确保队列不为空，否则会引发错误。