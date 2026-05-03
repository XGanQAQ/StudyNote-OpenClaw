# Computer Science Study Notes

> 本仓库用于系统性整理 **计算机科学与技术（Computer Science, CS）** 相关的学习笔记与实践记录。  
> 目标不是零散记知识点，而是逐步构建一套 **可长期生长的计算机科学知识体系**。

---

## 一、整体哲学（Philosophy）

本目录遵循以下原则：

1. **以 CS 主干为核心**
   - 数据结构与算法
   - 计算机系统
   - 操作系统、网络、编译原理
   - 图形学、AI 等方向性领域

2. **区分“理论层”和“工程层”**
   - 理论：解释 *为什么* 计算机可以这样工作
   - 工程：解决 *如何* 把系统真正做出来

3. **硬件知识服务于“系统理解”，而非电子工程**
   - 硬件内容以“系统视角”为主
   - 不以电路设计或 EE 为目标

4. **允许方向并行发展**
   - 系统 / 游戏 / AI / 工程实践可以并行推进
   - 但在目录结构上保持清晰边界

---

## 二、目录总览

```text
CS
├─ 00-Overview
├─ 01-ProgrammingFoundations
├─ 02-DataAndAlgorithms
├─ 03-ComputerSystems
├─ 04-SoftwareInfrastructure
├─ 05-NetworkAndDistributedSystems
├─ 06-GraphicsAndInteractive
├─ 07-AIAndData
├─ 08-EngineeringAndPractice
└─ 09-ProjectsAndNotes
````

---

## 三、各模块说明

### 00-Overview｜全局视角

用于描述整体 CS 知识结构与学习边界。

- CS 学科全景理解
    
- 各模块的定位说明
    
- 学习路线与阶段性总结
    

---

### 01-ProgrammingFoundations｜编程基础

**“如何表达计算逻辑”**

- ProgrammingLanguages：语言特性、语法与抽象
    
- ProgrammingParadigms：面向对象、函数式、过程式等
    
- DesignPatterns：常见架构与设计经验
    

该部分关注 _思维方式_，而非具体语言技巧。

---

### 02-DataAndAlgorithms｜数据与算法

**“如何高效地组织与处理信息”**

- DataStructures：结构的选择与权衡
    
- Algorithms：问题求解与复杂度分析
    

这是 CS 的核心能力层，与具体应用领域无关。

---

### 03-ComputerSystems｜计算机系统（核心）

**“程序如何真正运行在机器上”**

- HardwareBasics  
    电与信号、基础电子元件、硬件直觉  
    _用于支撑系统理解，不等同电子工程_
    
- DigitalLogic  
    逻辑门、时序、状态机等数字系统直觉
    
- ComputerOrganization  
    CPU、内存、指令系统、流水线等
    
- OperatingSystems  
    进程、线程、内存管理、文件系统
    
- EmbeddedSystems  
    MCU、外设、中断、嵌入式编程实践
    

该模块连接 **抽象的软件世界** 与 **真实的物理机器**。

---

### 04-SoftwareInfrastructure｜软件基础设施

**“支撑大型软件系统运转的底层机制”**

- Compilers：语言如何变成可执行程序
    
- Databases：数据存储与查询系统
    
- Runtime / VM：运行时系统、虚拟机模型
    

关注“平台级”而非具体业务。

---

### 05-NetworkAndDistributedSystems｜网络与分布式

**“多台计算机如何协同工作”**

- ComputerNetworks：协议、通信模型
    
- DistributedSystems：一致性、容错、扩展性
    

是后端、联机游戏、云系统的理论基础。

---

### 06-GraphicsAndInteractive｜图形与交互

**“计算机如何生成与呈现世界”**

- ComputerGraphics：数学与渲染原理
    
- GameAndEngine：引擎结构、实时系统、交互设计
    

该模块偏向实时性与视觉系统。

---

### 07-AIAndData｜人工智能与数据

**“计算机如何‘学习’与决策”**

- ArtificialIntelligence：搜索、推理、规划
    
- MachineLearning：统计学习与模型
    

该模块作为方向性扩展存在，不侵占 CS 主干。

---

### 08-EngineeringAndPractice｜工程实践

**“把系统真正落地”**

- DotNet / Frontend：具体技术栈
    
- DevOps：构建、部署、运维
    
- Tools：工程工具与效率系统
    

该部分强调实践与可交付能力。

---

### 09-ProjectsAndNotes｜项目与实验

**“知识的综合应用”**

- SystemProjects：系统向项目
    
- GameProjects：游戏 / 图形相关项目
    
- Experimental：探索性实验
    

用于沉淀跨模块经验。

---

## 四、关于硬件与电子内容的说明

本仓库中的硬件相关内容：

- 归属于 **ComputerSystems**
    
- 目标是理解：
    
    - 程序如何与硬件交互
        
    - 系统为何这样设计
        
- 不以电路设计或电子工程为主线
    

可视为 **CS 系统层的实践补充**。

---

## 五、持续维护原则

- 不追求“全”，而追求“结构正确”
    
- 允许内容不完整，但目录必须清晰
    
- 定期回顾并调整模块边界
    

---

> **计算机科学不是一门“记忆学科”，  
> 而是一套关于“抽象、系统与现实”的理解方式。**