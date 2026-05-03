## Unity Input System 层级结构总结

---

### 1. Input System (输入系统) - **基础框架**

- **这是什么？** 它指的是 Unity 引擎内置的**整个输入框架和底层逻辑**。它不是一个你能直接创建或配置的文件，而是一个在幕后运行的服务，负责与操作系统和硬件交互，获取原始输入数据。
    
- **主要职责：**
    
    - **设备管理：** 识别和管理连接的输入设备（键盘、鼠标、触摸屏、游戏手柄、传感器等）。
        
    - **原始数据：** 收集来自这些设备的原始输入信号。
        
    - **全局设置与调试：** 提供整个输入系统的全局配置（通过 `Project Settings -> Input System`）和强大的调试工具（`Window -> Analysis -> Input Debugger`）。
        
- **平台区分？** 在这个层级不直接进行平台区分。它是一个**通用层**，负责处理所有设备的通用输入流。
    

---

### 2. InputActions (输入动作资源) - **配置核心**

- **这是什么？** 这是一个**`.inputactions` 文件**，你通过 Unity 编辑器创建和配置它。它是你所有自定义输入逻辑的**中心存储库**。
    
- **主要职责：**
    
    - **容器：** 包含你的所有 **Action Maps** 和 **Actions** 定义。
        
    - **绑定定义：** 明确每个 Action 如何被一个或多个具体输入控件触发。
        
    - **生成 C# 类：** 能够自动生成一个 C# 类，让你在脚本中方便地访问和使用定义的 Action。
        
- **平台区分？** **这里是进行 PC 和 Mobile 平台输入区分的理想场所。** 你可以在同一个 `.inputactions` 文件中定义：
    
    - **Control Schemes (控制方案)：** 为不同的设备组合（如“键盘鼠标” vs. “触摸屏”）定义独立的绑定集合。系统会根据连接设备自动或手动激活最合适的方案。
        
    - **独立 Action Maps (备选)：** 对于逻辑差异很大的平台，也可以创建完全独立的 Action Maps（例如 `Player_PC` 和 `Player_Mobile`），然后在运行时根据平台启用对应的 Map。但通常通过 Control Schemes 管理更推荐。
        

---

### 3. Action Maps (动作映射) - **行为分组**

- **这是什么？** 是 **Actions 的集合**，位于 InputActions 资源内部。它将一组相关的游戏行为逻辑地组织在一起。
    
- **主要职责：**
    
    - **上下文切换：** 让你能够根据游戏状态（例如“在游戏中”、“在菜单中”、“在驾驶模式”）**启用或禁用一整组相关的输入行为**。
        
    - **模块化：** 使你的输入配置更清晰，易于管理和理解。例如，你可以有一个 `Player` Map 负责角色移动和战斗，一个 `UI` Map 负责菜单导航。
        
- **平台区分？** 可以在这里创建平台特定的 Map（如 `Player_PC`），但这更多是**行为逻辑上的区分**，而非设备区分。同一个 `Player` Map 可以在其内部通过 **Control Schemes** 拥有针对 PC 和 Mobile 的不同绑定。
    

---

### 4. Actions (动作) - **抽象行为**

- **这是什么？** 位于 Action Map 内部，代表游戏中一个**独立的、抽象的玩家行为**。它是你游戏逻辑的直接接口。
    
- **主要职责：**
    
    - **意图表达：** 定义“玩家想要做什么”（例如 `Jump`、`Move`、``Shoot`），而**不关心具体通过什么设备或按键来实现**。
        
    - **触发点：** 是你在脚本中监听事件（`performed`、`started`、`canceled`）或读取值（`ReadValue<T>()`）的对象。
        
    - **行为类型：** 可以是 `Button` (按下/抬起)、`Value` (连续变化的值，如移动方向)、`Pass-Through` (直接透传原始数据)。
        
    - **交互与处理器：** 可以配置 `Interactions` (例如 `Hold` 按住触发) 和 `Processors` (例如 `Normalize` 向量归一化) 来细化行为的触发条件和数据处理。
        
- **平台区分？** **Action 本身不区分平台。** `Jump` 动作在 PC 和 Mobile 上的含义都是“跳跃”。**区分体现在它的 Bindings (绑定) 上**：在 PC 上，它可能绑定到键盘的 `Space` 键；在 Mobile 上，它可能绑定到屏幕上的虚拟按钮或触摸手势。
    

---

### 简要总结层级关系：

Input System 是整个基础框架，它管理设备并收集原始输入。

一个 InputActions 文件是所有输入配置的中心，它包含了多个 Action Maps。

每个 Action Map 组织了一组相关的 Actions。

每个 Action 定义了一个抽象的游戏行为，并通过其绑定 (Bindings) 连接到具体的输入控件，而这些绑定可以根据 Control Schemes 进行区分，从而实现对不同设备和平台的适配。

---

## Input System 的主要调用方法总结

Unity Input System 在 C# 脚本中主要通过以下几种方式与你定义的 **Input Actions** 进行交互：

### 1. 使用 `PlayerInput` 组件 (最简单，推荐初学者)

`PlayerInput` 是一个内置的 MonoBehaviour 组件，它为你自动化了大部分 Input System 的设置和管理工作。

- **挂载位置：** 直接添加到你的玩家或任何需要处理输入的 GameObject 上。
    
- **配置方式：** 在 Inspector 中将你的 `.inputactions` 文件拖拽到 `Actions` 字段。
    
- **行为模式 (`Behavior` 属性)：**
    
    - **`Send Messages` (发送消息)：**
        
        - **原理：** 当一个 Action 触发时，`PlayerInput` 会自动在挂载了它的 GameObject 上寻找并调用一个特定命名的方法。
            
        - **方法命名规则：** `On` + `Action名称`。例如，如果你的 Action 叫 `Jump`，它会调用 `OnJump()`。如果 Action 是 `Value` 类型（如 `Move`），方法签名通常是 `OnMove(InputValue value)`。
            
        - **优点：** 非常简单直观，适合快速原型开发或简单的单玩家控制。
            
        - **缺点：** 耦合度较高，所有输入逻辑必须在同一个 GameObject 上。
            
        
        C#
        
        ```
        // 示例：PlayerInput 组件配置为 Send Messages
        public class MyPlayerController : MonoBehaviour
        {
            public void OnJump() // Action "Jump"
            {
                Debug.Log("跳跃！");
            }
        
            public void OnMove(InputValue value) // Action "Move" (Value类型)
            {
                Vector2 moveDirection = value.Get<Vector2>();
                Debug.Log("移动方向: " + moveDirection);
            }
        }
        ```
        
    - **`Invoke Unity Events` (调用 Unity 事件)：**
        
        - **原理：** 类似于传统的 Unity Event，你可以在 Inspector 中将其他脚本的方法拖拽到事件列表中。
            
        - **配置方式：** 在 Inspector 中，展开对应的 Action，然后为 `Started`、`Performed`、`Canceled` 事件添加监听器。
            
        - **优点：** 视觉化配置，可以轻松连接不同 GameObject 上的方法。
            
        - **缺点：** 不适合大量或动态的事件连接。
            
    - **`Invoke C# Events` (调用 C# 事件)：**
        
        - **原理：** `PlayerInput` 组件在内部订阅了生成的 C# 类的事件，然后通过其公共属性暴露出来，让你在代码中订阅这些事件。
            
        - **优点：** 结合了组件的便捷管理和 C# 事件的灵活性，代码逻辑更清晰。
            

---

### 2. 手动实例化和管理 (最灵活，推荐进阶使用)

这种方式需要你在脚本中手动创建和管理 `PlayerInputActions` 类的实例，并订阅其事件。

- **实现步骤：**
    
    1. 在脚本中声明一个 `PlayerInputActions` 类型的私有变量。
        
    2. 在 `Awake()` 或 `Start()` 中实例化这个变量：`playerInputActions = new PlayerInputActions();`
        
    3. 订阅你感兴趣的 Action 的事件（`performed`、`started`、`canceled`）。
        
    4. 在 `OnEnable()` 中启用 Action Map：`playerInputActions.YourActionMapName.Enable();`
        
    5. 在 `OnDisable()` 中禁用 Action Map：`playerInputActions.YourActionMapName.Disable();`
        
    6. 在 `OnDestroy()` 中取消事件订阅并销毁实例（`Dispose()`）以防止内存泄漏。
        
- **优点：**
    
    - **完全控制：** 对输入生命周期和行为有最大化的控制。
        
    - **多玩家/复杂场景：** 适合本地多玩家游戏、动态切换输入方案或需要跨多个脚本共享输入逻辑的场景。
        
    - **性能：** 事件驱动，避免在 `Update` 中频繁轮询。
        
- **缺点：** 需要更多的手动管理代码。
    
- **主要方法：**
    
    - **订阅事件：**
        
        - `YourAction.performed += context => YourMethod(context);` (动作执行完成，这是最常用的)
            
        - `YourAction.started += context => YourMethod(context);` (动作刚开始触发)
            
        - `YourAction.canceled += context => YourMethod(context);` (动作被取消或结束)
            
        - `InputAction.CallbackContext context` 参数包含了触发事件的 Action 的各种信息，如 `context.ReadValue<T>()` 获取值、`context.action.name` 获取 Action 名称等。
            
    - **读取当前值：**
        
        - `YourAction.ReadValue<T>()`：直接读取 Action 的当前值（例如 `Vector2` 用于移动方向，`float` 用于油门）。
            
        - `YourAction.IsPressed()`：检查按钮 Action 是否当前被按下。
            
        - `YourAction.WasPressedThisFrame()`：检查按钮 Action 是否在本帧被按下。
            
        - `YourAction.WasReleasedThisFrame()`：检查按钮 Action 是否在本帧被释放。
            
    - **启用/禁用 Action Map：**
        
        - `YourActionMap.Enable()`：激活一个 Action Map，使其开始接收输入。
            
        - `YourActionMap.Disable()`：禁用一个 Action Map，使其停止接收输入。
            
- **示例：**
    
    C#
    
    ```
    using UnityEngine;
    using UnityEngine.InputSystem;
    
    public class ManualInputManager : MonoBehaviour
    {
        private PlayerInputActions playerActions; // 假设你生成的C#类名为 PlayerInputActions
        private Vector2 currentMoveInput;
    
        void Awake()
        {
            playerActions = new PlayerInputActions();
    
            // 订阅移动事件 (Value Action)
            playerActions.Player.Move.performed += ctx => currentMoveInput = ctx.ReadValue<Vector2>();
            playerActions.Player.Move.canceled += ctx => currentMoveInput = Vector2.zero;
    
            // 订阅跳跃事件 (Button Action)
            playerActions.Player.Jump.performed += ctx => Debug.Log("手动处理：跳跃！");
        }
    
        void OnEnable()
        {
            playerActions.Player.Enable(); // 启用 Player Action Map
        }
    
        void OnDisable()
        {
            playerActions.Player.Disable(); // 禁用 Player Action Map
        }
    
        void OnDestroy()
        {
            // 取消订阅并销毁实例
            playerActions.Player.Move.performed -= ctx => currentMoveInput = ctx.ReadValue<Vector2>();
            playerActions.Player.Move.canceled -= ctx => currentMoveInput = Vector2.zero;
            playerActions.Player.Jump.performed -= ctx => Debug.Log("手动处理：跳跃！");
            playerActions.Dispose();
        }
    
        void Update()
        {
            // 在 Update 中使用读取到的输入值
            transform.Translate(new Vector3(currentMoveInput.x, 0, currentMoveInput.y) * Time.deltaTime * 5f);
        }
    }
    ```
    

---

### 3. 直接查询设备 (不常用，除非是特殊情况)

Input System 也可以让你直接查询连接的设备和它们的控件，但这通常不如通过 Actions 来得抽象和方便。

- **使用场景：** 极少数情况下，当你需要访问特定设备的原始数据，或者实现非常底层的输入功能时。
    
- **主要方法：**
    
    - `Keyboard.current.spaceKey.wasPressedThisFrame`
        
    - `Mouse.current.leftButton.isPressed`
        
    - `Gamepad.current.leftStick.x.ReadValue()`
        
    - `Touchscreen.current.primaryTouch.position.ReadValue()`
        
- **缺点：** 失去了 Input System 的主要优势（抽象、可重绑定、多设备兼容）。
    

---

### 总结选择指南

- **简单单玩家控制**：使用 **`PlayerInput` 组件**并配置为 `Send Messages` 或 `Invoke Unity Events`。这是最快上手的方式。
    
- **复杂多玩家或高级控制逻辑**：**手动实例化和管理 Input Actions 类**，并订阅其 C# 事件。这提供了最大的灵活性和控制力。
    
- **极少数底层需求**：直接查询 **`InputSystem.current`** 下的设备和控件。
    

理解这些调用方法能帮助你根据项目的复杂度和需求，选择最合适的 Input System 使用方式。