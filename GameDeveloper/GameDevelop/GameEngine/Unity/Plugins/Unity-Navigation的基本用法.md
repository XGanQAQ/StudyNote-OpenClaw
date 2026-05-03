- Navigation Mesh Surface 烘培地面
- Navigation Modify 对烘培的物体做额外的修改
- Navigation Agent 让物体根据烘培的网格地面进行寻路

Unity 自带的 **Navigation** 插件主要用于 **AI 寻路**，核心是 `NavMesh`（导航网格）、`NavMeshAgent`（寻路代理）和 `NavMeshObstacle`（障碍物）。

---

## 🚀 1. 基本概念

- **NavMesh**：在场景中烘焙出来的可行走区域。
    
- **NavMeshAgent**：挂在角色上的组件，让角色能沿着 NavMesh 自动寻路。
    
- **NavMeshObstacle**：动态障碍物，比如推箱子、门，会阻挡 AI 行走。
    

---

## 🛠️ 2. 基本示例步骤

### Step 1. 场景准备

1. 新建一个 Unity 场景。
    
2. 在场景中创建一些地形：
    
    - **Plane**（作为地面）。
        
    - **Cube**（放几个当障碍物）。
        

---

### Step 2. 生成导航网格 NavMesh

1. 选中地面（Plane），在 **Inspector** 里添加 **Navigation Static**。
    
    - 方式：勾选 `Static → Navigation Static`。
        
2. 打开 **Navigation 窗口**：`Window → AI → Navigation`。
    
3. 在 **Bake** 选项卡里，点击 **Bake** → Unity 会生成可行走区域（蓝色）。
    

---

### Step 3. 创建 AI 角色

1. 新建一个 **Cube** 或 **Capsule**（作为角色）。
    
2. 给它添加 **NavMeshAgent** 组件。
    
    - 可以调节 **Speed（速度）**、**Angular Speed（转向速度）**、**Stopping Distance（停止距离）**。
        

---

### Step 4. 编写简单寻路脚本

在角色上新建脚本 `AgentMove.cs`：

```csharp
using UnityEngine;
using UnityEngine.AI;

public class AgentMove : MonoBehaviour
{
    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        // 鼠标点击地面，角色移动过去
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out RaycastHit hit))
            {
                agent.SetDestination(hit.point);
            }
        }
    }
}
```

> 这样，当你运行游戏，点击地面时，角色会自动寻路到点击位置 🚶。

---

### Step 5. 添加动态障碍物（可选）

1. 给场景中的 **Cube** 添加 **NavMeshObstacle** 组件。
    
2. 设置 `Carve = true`，让它在 NavMesh 上挖洞，阻挡 AI 的路径。
    
3. 运行时，你会看到角色会绕开障碍物。
    

---

## 📌 3. 常见问题

- 如果角色 **不动**：检查是否正确 **烘焙 NavMesh**，并且点击的地方在可行走区域。
    
- 如果角色 **穿过障碍物**：记得给障碍物加 `NavMeshObstacle` 并勾选 **Carve**。
    
- 如果角色 **移动不平滑**：调整 `NavMeshAgent` 的 **Acceleration** 和 **Angular Speed**。
    

---

## ✅ 4. 总结

- **静态场景 → NavMesh 烘焙**。
    
- **角色 → NavMeshAgent**。
    
- **障碍物 → NavMeshObstacle**。
    
- **代码控制寻路 → `agent.SetDestination(Vector3)`**。
    