程序集 Core.UI

## 架构

### MVP 架构
- **适用情景：** 游戏中的**主菜单**、**设置界面**、**库存（背包）系统**、**角色状态面板**、**任务日志**、**商店**等。
- **为什么适用：** 这些界面通常涉及复杂的数据处理（Model）、状态管理和视图更新（Presenter），以及大量的用户交互（View）。
    - **Model:** 包含角色的属性数据、物品列表、任务状态等。
	    - Gameplay程序集
	    - MonoBehaviour脚本
    - **Presenter:** 接收 View 的点击事件，调用 Model 来修改数据，然后指示 View 更新显示。
	    - UI程序集
	    - 普通的 C# 类 (POCO)
	    - Presenter 的实例作为 **View (一个 `MonoBehaviour`)** 脚本的私有成员
    - **View:** 仅负责显示 UI 元素和捕捉用户输入，对业务逻辑一无所知。
	    - UI程序集
	    - MonoBehaviour脚本
- **优势：** 可以轻松修改界面布局（View）而不影响底层数据和逻辑（Model 和 Presenter），反之亦然。

### 事件总线
传递跨模块消息
- 可以让Gameplay里用事件总线，发出打开某个UI的消息

### UIManager 中心UI管理器
统筹管理所有的UI，实现一些保护所有UI的功能
- ECS快捷关闭当前最上方的窗口UI
- 将输入绑定到对应的UI
	- Unity的InputSystem
- 控制鼠标的锁定 游戏的暂停 人物的暂停
	- 利用事件总线

## 📜 依赖关系示例（单向依赖）

为了保持您的 **Gameplay** 程序的纯净和独立，您需要使用**接口 (Interface)** 来实现 Model 和 View 之间的通信。

### 1. Gameplay 程序集

- 包含：`PlayerModel` (Model)
    
- 定义：`IPlayerData` (Model 的数据接口)
    

### 2. UI 程序集

- 包含：`PlayerPanel` (View)、`PlayerPanelPresenter` (Presenter)
    
- 定义：`IPlayerPanelView` (View 的接口)
    

**工作流程：**

1. **View (UI)** 实例化 **Presenter (UI)**，并将自身的接口 (`IPlayerPanelView`) 传递给 Presenter。
    
2. **Presenter (UI)** 接收到 View 接口和 **Model (Gameplay)** 实例。
    
3. View 上的按钮被点击，View 调用 Presenter 上的方法，例如 `presenter.OnAttackButtonClicked()`。
    
4. Presenter 调用 Model 上的方法，例如 `model.PerformAttack()`。
    
5. Model 数据发生变化后，Model 可以通过**事件总线**或**回调**通知 Presenter。
    
6. Presenter 接收到通知，调用 View 接口上的方法，例如 `view.UpdateHealthBar(newHealth)`。

Presenter如何获得Model实例？ #TODO


## 实现

### 核心类 Old
- UIManager 
	- UI管理器
	- 职责：管理全局UI，动态加载UI预制体，开关UI的入口
	- 单例 统一 UI管理入口
- UILayer
	- 枚举类型
		- Background  
		- Normal 
		- Popup
		- Top
	- 定义了4种UI层级
- UILayerRoot
	- UI层级根节点
	- 管理其根节点之下的UIBase
	- 通过Manager服务定位器来获得UIManager，然后将自己注册到UIManager当中
- UIBase 
	- 所有UI的基类
- UICamera
	- 只负责渲染UI要素

### 设想
由于不同的游戏类型，对于UI的需求也不同，但是大概可以都需要如下所示的功能
- ECS快捷关闭当前最上方的窗口UI
- 将输入绑定到对应的UI
	- Unity的InputSystem
- 控制鼠标的锁定 游戏的暂停 人物的暂停
	- 利用事件总线

有一种方法是把这些功能划分为纯c#类，UIManager作为Gameplay的实例，如何其中有对应功能的字段。


