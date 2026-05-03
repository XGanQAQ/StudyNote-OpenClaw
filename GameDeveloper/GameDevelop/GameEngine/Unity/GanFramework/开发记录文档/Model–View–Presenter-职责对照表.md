# Unity MVP 职责总表（核心）

| 层                 | 核心职责        | **应该做的事（✓）**                                                                             | **绝对不该做的事（✗）**                                                                               |
| ----------------- | ----------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Model**         | **游戏规则与数据** | ✓ 保存游戏状态（HP、金币、卡组）<br>✓ 规则计算（伤害、结算、概率）<br>✓ 状态合法性校验<br>✓ 可序列化 / 存档<br>✓ 可单元测试            | ✗ 继承 MonoBehaviour<br>✗ 引用 UnityEngine<br>✗ 操作 Transform / Animator<br>✗ 播放音效 / 特效<br>✗ 处理输入 |
| **View (Viewer)** | **表现与交互**   | ✓ 场景物体（角色、敌人、建筑）<br>✓ UI 显示（文本、血条、按钮）<br>✓ 播动画 / 特效<br>✓ 接收输入、碰撞、点击<br>✓ 转发事件给 Presenter | ✗ 写游戏规则<br>✗ 直接改 Model 数据<br>✗ 复杂 if/else 逻辑<br>✗ 决定“该不该发生”                                  |
| **Presenter**     | **业务逻辑与协调** | ✓ 接收 View 事件<br>✓ 调用 Model 修改状态<br>✓ 决定流程（死亡、胜负、结算）<br>✓ 通知 View 更新显示<br>✓ 作为唯一通信桥梁      | ✗ 继承 MonoBehaviour（一般）<br>✗ 直接操作 Animator/Transform<br>✗ 存 Unity 组件引用（除接口）                   |

---

## 一句话版（强烈建议记住）

|层|一句话职责|
|---|---|
|**Model**|_“世界规则是什么”_|
|**Presenter**|_“现在该发生什么”_|
|**View**|_“把它演出来，并告诉我你点了什么”_|

---

## Unity 中的「典型归属速查表」

### 属于 **Model**

- 角色属性（HP / 攻击 / 防御）
    
- 卡牌数据、卡牌效果结算
    
- 金币、经验、等级
    
- 状态机（逻辑状态）
    
- 存档数据
    
- 战斗结果判定
    

---

### 属于 **View**

- 角色 GameObject
    
- Animator / VFX / AudioSource
    
- UI Text / Slider / Button
    
- NavMeshAgent
    
- 碰撞体、射线检测
    
- 摄像机控制（表现层）
    

---

### 属于 **Presenter**

- “点击攻击按钮 → 计算伤害 → 扣血 → 播动画”
    
- “HP 归零 → 播死亡 → 掉落 → 通知 UI”
    
- “回合开始 / 结束”
    
- “是否允许出牌”
    
- “当前状态是否可交互”
    

---

## 常见「边界模糊」问题速判

### ❓Transform 属于哪一层？

➡ **View**

> Presenter：`MoveTo(pos)`

---

### ❓Animator 状态机？

➡ **View**

> Presenter 决定播哪个状态

---

### ❓状态机（Idle / Attack / Dead）？

- **逻辑状态** → Model / Presenter
    
- **动画状态** → View
    

---

### ❓碰撞 / OnTriggerEnter？

➡ **View 接收 → Presenter 决策**

```csharp
void OnTriggerEnter(Collider other)
{
    presenter.OnHit(other);
}
```

---

## MVP 通信方向（硬规则）

```
View  ──事件──▶ Presenter ──调用──▶ Model
Model ──数据──▶ Presenter ──更新──▶ View
```

❌ View ↔ Model  
❌ Model ↔ View  
❌ View 自己做决策

---

## Unity 项目中推荐的文件结构

```text
Battle/
├── Model/
│   └── EnemyModel.cs
├── Presenter/
│   └── EnemyPresenter.cs
├── View/
│   ├── EnemyView.cs
│   └── EnemyUIView.cs
```

---

## 一个「自检清单」（非常实用）

当你写一个类时，问自己：

1. **没有 Unity 还能运行吗？**
    
    - 能 → Model / Presenter
        
    - 不能 → View
        
2. **它是在“决定”还是“表演”？**
    
    - 决定 → Presenter
        
    - 表演 → View
        
3. **删掉它会不会改变规则？**
    
    - 会 → Model
        
    - 不会 → View
        