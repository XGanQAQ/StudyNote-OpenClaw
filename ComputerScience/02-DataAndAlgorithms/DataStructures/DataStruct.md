# 数据结构

## 线性结构
- **数组 (Array)**：连续内存，随机访问 O(1)
- **链表 (LinkedList)**：非连续，插入删除 O(1)
- **栈 (Stack)**：后进先出 (LIFO)
- **队列 (Queue)**：先进先出 (FIFO)

## 哈希表 (HashTable)
- [哈希表基础](Hash/哈希表.md)
- [哈希冲突处理](Hash/哈希冲突.md)
- [哈希函数构建](Hash/哈希函数的构建方法.md)

## 树 (Tree)
- [树的定义](Tree/TreeDefinition.md)
- [二叉树](Tree/BinaryTree.md)
- [树与森林](Tree/ForestAndTrees.md)
- [树的算法](Tree/TreeAlogrithm.md)
- [树的存储](Tree/TreeStorge.md)

### 树的应用
| 类型 | 特点 | 用途 |
|------|------|------|
| 二叉搜索树 (BST) | 左<根<右 | 快速查找 |
| 平衡二叉树 (AVL) | 左右子树高度差≤1 | 避免退化 |
| 红黑树 | 近似平衡 | C++ map/set 底层 |
| B/B+ 树 | 多路搜索树 | 数据库索引 |
| 堆 (Heap) | 完全二叉树 | 优先队列 |

## 图 (Graph)
- [图的定义](Graph/图的定义与术语.md)
- [图的存储](Graph/图的存储结构.md)
- [图的遍历](Graph/图的遍历.md)
- [拓扑排序](Graph/拓扑排序.md)
- [最小生成树](Graph/最小生成树.md)
- [最短路径 Dijkstra](Graph/最短路径Dijkstra算法.md)
- [图的连通性](Graph/图的连通性问题.md)

## 查找
- [静态查找表](Set/静态查找表.md)
- [索引顺序表](Set/索引顺序表.md)
