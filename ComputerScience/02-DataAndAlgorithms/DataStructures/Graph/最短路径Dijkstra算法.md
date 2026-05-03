**Dijkstra算法** 是一种用于寻找加权图中从起点到其他所有顶点的最短路径的经典算法，由计算机科学家 **Edsger W. Dijkstra** 提出。它在路径规划、网络路由、交通导航等领域有广泛应用。

### **算法特点**
- 适用于 **非负权重图**（边权重不能为负）。
- 时间复杂度：  
  - 使用简单数组实现的版本为 \(O(V^2)\)，其中 \(V\) 是图中顶点数。
  - 使用优先队列（如二叉堆）实现的版本为 \(O((V + E) \log V)\)，其中 \(E\) 是边数。

---

### **算法思想**
1. **初始化**：
   - 将起点的距离设为 0，其他所有顶点的距离设为无穷大（∞）。
   - 使用一个优先队列或集合来存储当前未处理的节点。
2. **选择当前最短路径顶点**：
   - 从未处理的顶点中选取距离起点最近的顶点。
3. **更新相邻顶点的距离**：
   - 对于当前顶点的每一条边，如果通过该顶点到达某个相邻顶点的距离小于当前记录的距离，则更新该距离。
4. **重复**：
   - 重复上述步骤，直到所有顶点都被处理或优先队列为空。

### **实现**
1. 维护3个数组
   - `visited[]`：标记顶点是否已已经处理。
   - `dist[]`：记录起点到每个顶点的最短距离。
   - `parent[]`：记录每个顶点的前驱节点，用于还原路径。
2. 每次从未处理的数组中，找到距离起点最近的节点，进行处理，加入到最优先路径中。
3. 计算刚加入的节点的临近节点距离，如果新加入的最新距离小于旧距离，则更新最短距离和该节点的前驱节点。

---

以下是基于您描述的实现要求，使用C++编写的 Dijkstra 算法。这个实现使用了 `visited[]`、`dist[]` 和 `parent[]` 数组来标记处理状态、记录最短距离、还原路径。

```cpp
#include <iostream>
#include <vector>
#include <climits>
#include <queue>

using namespace std;

const int INF = INT_MAX;  // 定义一个大的常数，表示无限大（无穷大）

// 结构体表示图的边 (节点, 权重)
struct Edge {
    int to, weight;
    Edge(int _to, int _weight) : to(_to), weight(_weight) {}
};

// Dijkstra算法实现
void dijkstra(const vector<vector<Edge>>& graph, int start) {
    int n = graph.size();  // 图中顶点的数量
    vector<int> dist(n, INF);      // 最短距离数组
    vector<int> parent(n, -1);     // 记录每个节点的前驱节点
    vector<bool> visited(n, false); // 标记每个节点是否已处理

    dist[start] = 0;  // 起点的最短路径为0
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    pq.push({0, start});  // 将起点加入优先队列，格式是 (距离, 节点)

    while (!pq.empty()) {
        // 获取当前距离最小的节点
        int u = pq.top().second;
        pq.pop();

        // 如果该节点已处理过，跳过
        if (visited[u]) continue;

        visited[u] = true;

        // 遍历 u 的所有邻接节点
        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            int weight = edge.weight;

            // 如果经过 u 到 v 的距离更短，更新 dist[v] 和 parent[v]
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                parent[v] = u;
                pq.push({dist[v], v});  // 将更新后的节点加入优先队列
            }
        }
    }

    // 输出最短路径的距离
    for (int i = 0; i < n; ++i) {
        if (dist[i] == INF) {
            cout << "从节点 " << start << " 到节点 " << i << " 没有路径\n";
        } else {
            cout << "从节点 " << start << " 到节点 " << i << " 的最短距离是: " << dist[i] << "\n";
        }
    }

    // 输出路径
    for (int i = 0; i < n; ++i) {
        if (dist[i] != INF) {
            cout << "从 " << start << " 到 " << i << " 的路径: ";
            int node = i;
            while (node != -1) {
                cout << node << " ";
                node = parent[node];
            }
            cout << endl;
        }
    }
}

int main() {
    // 创建一个图，图是一个邻接表表示的有向加权图
    int n = 5; // 图的顶点数
    vector<vector<Edge>> graph(n);

    // 添加边 (从节点u到节点v, 权重w)
    graph[0].push_back(Edge(1, 1));  // 0 -> 1，权重为 1
    graph[0].push_back(Edge(2, 4));  // 0 -> 2，权重为 4
    graph[1].push_back(Edge(2, 2));  // 1 -> 2，权重为 2
    graph[1].push_back(Edge(3, 5));  // 1 -> 3，权重为 5
    graph[2].push_back(Edge(3, 1));  // 2 -> 3，权重为 1
    graph[3].push_back(Edge(4, 3));  // 3 -> 4，权重为 3

    int start = 0; // 起点是节点0

    dijkstra(graph, start);  // 调用 Dijkstra 算法

    return 0;
}
```

### **代码解释**
1. **图的表示**：  
   - 使用 `vector<vector<Edge>>` 来表示图，其中 `Edge` 结构体存储目标节点 `to` 和边的权重 `weight`。
   
2. **Dijkstra 算法实现**：  
   - 使用一个最小堆（`priority_queue`）来动态选择当前未处理的、距离起点最近的节点。
   - 对每个节点进行处理时，更新它的邻接节点的最短距离和前驱节点。
   
3. **输出**：  
   - 最终输出从起点到所有节点的最短距离，并且使用 `parent[]` 数组来还原路径。

### **示例图**
假设图如下：
```
    A --1--> B --2--> D
     \       |
      4      3
       \     v
        > C --1--> D
```
对于起点 A，输出将是：
```
从节点 0 到节点 0 的最短距离是: 0
从节点 0 到节点 1 的最短距离是: 1
从节点 0 到节点 2 的最短距离是: 3
从节点 0 到节点 3 的最短距离是: 4
从节点 0 到节点 4 的最短距离是: 7

从 0 到 1 的路径: 0 1 
从 0 到 2 的路径: 0 1 2 
从 0 到 3 的路径: 0 1 2 3 
从 0 到 4 的路径: 0 1 2 3 4
```

这个实现可以通过修改输入图来处理不同的场景。