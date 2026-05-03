在C++中，`stack`是一种适合**后进先出 (LIFO)** 操作的数据结构，常用于需要按顺序压入、弹出数据的情景，比如深度优先搜索 (DFS)、括号匹配等。C++ 标准库的 `stack` 类位于 `<stack>` 头文件中。以下是 `stack` 类的常用方法：

### 1. 基本操作

- **`push`**：将元素压入栈顶。
    ```cpp
    stack<int> s;
    s.push(10);  // 将 10 压入栈顶
    s.push(20);  // 将 20 压入栈顶
    ```

- **`pop`**：移除栈顶元素。注意：`pop`不会返回被删除的元素。如果需要获取栈顶元素的值，可以先使用 `top` 方法。
    ```cpp
    s.pop();  // 删除栈顶元素
    ```

- **`top`**：返回栈顶元素的引用，可以用于读取或修改栈顶元素。
    ```cpp
    int x = s.top();  // 获取栈顶元素，不删除
    s.top() = 30;     // 修改栈顶元素
    ```

- **`empty`**：检查栈是否为空。如果栈为空，则返回 `true`；否则返回 `false`。
    ```cpp
    if (s.empty()) {
        cout << "Stack is empty!" << endl;
    }
    ```

- **`size`**：返回栈中元素的个数。
    ```cpp
    int n = s.size();  // 获取栈中元素数量
    ```

### 2. 示例代码

以下是一个使用 `stack` 的例子，实现了简单的括号匹配检查：

```cpp
#include <iostream>
#include <stack>
#include <string>

using namespace std;

bool isValidParentheses(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') {
            st.push(c);  // 左括号入栈
        } else {
            if (st.empty()) return false;  // 如果栈空，说明没有匹配的左括号
            char top = st.top();
            if ((c == ')' && top == '(') ||
                (c == '}' && top == '{') ||
                (c == ']' && top == '[')) {
                st.pop();  // 成对匹配的括号出栈
            } else {
                return false;
            }
        }
    }
    return st.empty();  // 如果栈空，说明所有括号匹配成功
}

int main() {
    string s = "{[()]}";
    if (isValidParentheses(s)) {
        cout << "Parentheses are balanced!" << endl;
    } else {
        cout << "Parentheses are not balanced!" << endl;
    }
    return 0;
}
```

### 3. 注意事项
- **无随机访问**：`stack`不支持随机访问（如使用索引 `[]`），只能访问栈顶元素。
- **删除栈顶元素前应检查是否为空**：调用 `pop` 或 `top` 前应先确保栈不为空，否则会引发错误。