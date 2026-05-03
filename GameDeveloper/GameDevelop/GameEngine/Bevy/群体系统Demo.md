好，那我给你一份**可以直接开干的、纯 ECS 爽点取向的群体系统 Demo 策划案**。  
目标是：**不复杂、不卷表现、1–2 天能跑起来，但 ECS 特性非常明显**。

---

# 群体系统 Demo 策划案

**项目代号：Swarm Lab（群体实验室）**

> 一个用于观察「大量实体在简单规则下产生复杂行为」的 ECS Demo

---

## 一、Demo 核心目标（先定边界）

### 🎯 核心目标

- 同屏 **500–3000 个实体**
    
- 没有“主角”
    
- 没有剧情
    
- 没有关卡
    
- 一切行为来自 **System 规则**
    

### 🧠 学习重点

- Bevy ECS 的 **Query / System / Schedule**
    
- “组件决定能力”
    
- 系统叠加产生复杂行为
    
- 数据变化驱动现象变化
    

---

## 二、整体玩法概念（你在“玩”什么）

> 你不是在操作角色，而是在 **调规则参数，看世界如何变化**

你可以：

- 调整群体数量
    
- 开关某些 System
    
- 改变参数（速度、视野、伤害）
    
- 观察群体结构的变化
    

---

## 三、世界设定（极简）

### 🌍 世界

- 2D 平面（Bevy 2D）
    
- 无限或有限矩形空间
    
- 边界反弹 / 环绕
    

### 🔵 实体类型（只有三种）

|实体|说明|
|---|---|
|**Agent**|群体单位（圆点）|
|**Food**|静态资源|
|**Obstacle（可选）**|障碍物|

---

## 四、Entity & Component 设计（ECS 核心）

### 1️⃣ Agent 实体

```text
Agent
├─ Transform
├─ Velocity
├─ VisionRange
├─ Energy
├─ SteeringForce
├─ Faction（可选）
├─ Lifetime（可选）
```

#### 关键组件说明

|组件|作用|
|---|---|
|Velocity|当前运动方向|
|VisionRange|感知范围|
|Energy|生存资源|
|SteeringForce|本帧合力（系统写入）|
|Faction|群体类别（颜色）|

---

### 2️⃣ Food 实体

```text
Food
├─ Transform
├─ Nutrition
```

---

## 五、System 设计（这是重点）

> **每个 System 都非常简单，但叠加后会产生复杂行为**

---

### 🧠 感知类系统（只读世界）

#### 1️⃣ 邻居感知系统

**作用**

- 找到 VisionRange 内的其他 Agent
    
- 不做行为，只计算数据
    

**输出**

- 给 Agent 加临时数据（或写入 SteeringForce）
    

---

### 🧲 行为规则系统（写 SteeringForce）

#### 2️⃣ 分离（Separation）

> 避免过于拥挤

```text
距离近 → 反方向力
```

---

#### 3️⃣ 对齐（Alignment）

> 与邻居速度趋同

```text
邻居平均速度 → 调整自己
```

---

#### 4️⃣ 聚合（Cohesion）

> 向群体中心靠拢

```text
邻居平均位置 → 吸引力
```

👉 **这三者 = Boids 核心**

---

#### 5️⃣ 觅食系统（Food Seeking）

- Energy 低于阈值
    
- 朝最近 Food 施加力
    

---

#### 6️⃣ 能量消耗系统

- 移动消耗 Energy
    
- Energy ≤ 0 → 死亡
    

---

#### 7️⃣ 繁殖系统（可选）

- Energy ≥ 阈值
    
- Spawn 新 Agent
    
- 父体 Energy 减少
    

---

### 🧮 物理更新系统（统一结算）

#### 8️⃣ 合力结算系统

```text
Velocity += SteeringForce * dt
Transform += Velocity * dt
SteeringForce 清零
```

---

### 🧼 清理系统

- 删除死亡 Agent
    
- 删除被吃掉的 Food
    

---

## 六、参数驱动（Demo 的“可玩性”来源）

所有行为都来自参数：

```rust
struct SwarmParams {
    separation_weight: f32,
    alignment_weight: f32,
    cohesion_weight: f32,
    max_speed: f32,
    vision_radius: f32,
}
```

你可以：

- 改参数 → 行为立刻变化
    
- 关闭某个 System → 群体崩解
    

👉 **这正是 ECS + 数据驱动的爽点**

---

## 七、最小可运行版本（MVP）

### 第一阶段（2–3 小时）

- Agent + Velocity
    
- Separation / Alignment / Cohesion
    
- 1000 个点在跑
    

### 第二阶段（+2 小时）

- Food
    
- Energy
    
- 觅食 + 死亡
    

### 第三阶段（随缘）

- Faction（不同颜色）
    
- 不同参数的群体对比
    
- 繁殖
    

---

## 八、你不需要做的事情（请务必克制）

❌ UI 系统  
❌ 音效  
❌ 美术  
❌ 输入系统（最多一个 reset）  
❌ 完整碰撞系统

---

## 九、这个 Demo 对你真正的价值

你会在这个 Demo 中**真正理解**：

- 为什么 ECS 适合群体
    
- System 顺序的重要性
    
- 数据变化如何放大成“行为”
    
- “没有对象互相调用”的世界是怎么运转的
    

---

## 十、下一步我可以继续直接帮你落地

你可以直接选一个：

1️⃣ **我给你一个 Bevy 项目结构 + 系统注册顺序示例**  
2️⃣ **直接给你 Boids 三系统的 Bevy 代码骨架**  
3️⃣ **帮你把参数设计成“可实时调”的结构（无 UI 版）**

你选哪个？