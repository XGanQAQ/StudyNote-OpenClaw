
## Navigation 寻路
![](GAMES104-NavigationSteps.png)

### Map Representation - Walkable Area
告诉计算机哪些区域可以走

地图区域的表达方式
- Waypoint Network 路点网络
- Grid 网格
- Navigation Mesh 
	- 凸多边形
- Sparse Voxel Octree 八叉树
	- 空间分割寻路

Path Finding 寻路
- DFS
- BFS
- Dijkstra Algorithm
- A Start 算法
	- 启发函数

Path Smoothing
- Funnel Algorithm

NavMesh Generation - Voxelization

## Steering 转向系统

![](Steering-Behaviors.png)

## Crowd Simulation 群体模拟

- Microscopic Models
- Macroscpic models
- Mesoscopic models

### Collision Avoidance - Force-based Model

## Sensing or Perception 环境感知

- 自身状态
- Statoc Spatial Information 静态空间信息
	- Navigation Data
	- Tactical Map 战略点 
- Dynamic Spatial Information
	- Influence Map
	- Game Object

### Sensing Simulation

视觉 听觉

## Classic Decision Making Algorithms

- Finite State Machine
	- Hierarchical Finite State Machine 层次状态有限状态机
- Behaviour Tree

- Hierachical Tasks Network
- Goal Oritented Action Planning
- Monte Carlo Tree Search
- Deep Learning

### Behaviour Tree
- Condition Node
- Action Node

Control flow node
- Sequence 顺序执行
	- Plan
- Selector 选择
- Parallel 并行
- Decorator 

Tick a Behaviour Tree
- 每次从根节点tick
- 同时激活的节点可能多个