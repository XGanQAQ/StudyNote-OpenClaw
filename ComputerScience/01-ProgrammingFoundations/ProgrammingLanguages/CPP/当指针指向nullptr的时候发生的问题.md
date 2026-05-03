# 当指针指向nullptr的时候发生的问题
对比思考下述代码的区别，预测可能的结果

## 问题代码
```cpp
//请重点观察对于temp指针变量的赋值
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        TreeNode* root = new TreeNode(nums[0]);
        TreeNode* temp = root;
        temp = temp->right;
        root->left = new TreeNode(nums[1]);
        temp = new TreeNode(nums[1]);
        return root;
    }

    TreeNode* sortedArrayToBST(vector<int>& nums) {
        TreeNode* root = new TreeNode(nums[0]);
        TreeNode* temp = root;
        
        root->left = new TreeNode(nums[1]);
        temp->right = new TreeNode(nums[1]);
        return root;
    }
```
上述问题代码中，看似是对同样的指针指向的地址进行了赋值，可是俩段代码缺出现了不一样的结果，第一个存在问题，第二个没有问题。

## 基础知识复习（很关键）
为了更好的理解问题的原因，我们先复习一下与内存相关的基础知识

### 什么是nullptr
- `nullptr` 是一个关键字，代表空指针常量。它在 C++11 中引入，用于表示指针不指向任何有效对象或地址。
- 使用 `nullptr` 可以避免一些类型安全问题，因为它的类型是 `std::nullptr_t`，可以被隐式转换为任何指针类型。它比传统的 `NULL` 更安全，后者通常定义为 `0`，在某些情况下可能导致类型混淆。
#### 示例：
```cpp
int* ptr = nullptr; // ptr 是一个空指针，当前不指向任何对象
if (ptr == nullptr) {
    // 处理指针为空的情况
}
```


### 什么是new
- `new` 是一个运算符，用于在堆上动态分配内存。使用 `new` 时，系统会在运行时分配所需的内存，并返回指向该内存块的指针。
- `new` 操作符通常与构造函数一起使用，用于创建对象并初始化它们。使用 `new` 分配的内存需要手动释放，以防止内存泄漏，通常通过 `delete` 操作符来释放。
#### 示例：
```cpp
int* p = new int; // 在堆上分配一个 int 类型的内存，并返回指向它的指针
*p = 42; // 设置指向的内存值为 42

delete p; // 释放分配的内存
```

### 总结
- **`nullptr`**：表示空指针，不指向任何有效的内存地址，类型安全，避免类型混淆。
- **`new`**：用于**动态分配内存，创建对象并返回指向该对象的指针**，分配的内存需要通过 `delete` 释放。

## nullptr并不是一个存在的指针
### 第一段代码  
通过temp = temp->left  
先将指针切换到temp->left指针(temp->left是nullptr)  
再给temp的指针赋上开辟的树节点地址  
看似像给temp->left的指针赋上了新开辟的树节点地址  
但是
因为temp->left是nullptr空指针  
将temp 切换到空指针    
再给temp(就是空指针)赋上了新开辟的树节点地址  
是给空指针赋值上了新开辟的树节点地址
而非给temp->left树的左子树赋上新开辟的树节点地址  
所以说没能正确的构造树结构


### 第二段代码
通过直接给 temp->left 这个指针变量（树节点的一个成员变量）赋值上了新开辟的树节点地址 
正确的构造了树结构

## 总结
分清楚  
你是在给nullptr这个无效的空节点赋值  
还是给树节点赋值  
其实整理完后，感觉还是很怪，但是这可能就是cpp处理的特性吧