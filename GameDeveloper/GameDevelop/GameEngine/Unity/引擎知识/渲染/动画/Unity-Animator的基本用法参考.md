Unity Animator（动画控制器）是Unity中用来管理和控制动画状态和过渡的核心组件。下面是其基本用法的简要参考：

### 1. 创建和设置动画控制器

1. 创建 Animator Controller：
    
    在 Project 窗口中，右键点击 -> Create -> Animator Controller。给它一个名字，比如 "PlayerAnimator"。
    
2. 将 Animator Controller 附加到对象：
    
    选中你想要播放动画的 GameObject（比如一个角色模型），在 Inspector 窗口中，点击 Add Component，然后搜索 Animator。将你刚刚创建的 "PlayerAnimator" 拖到这个 Animator 组件的 Controller 字段中。
    

### 2. Animator 窗口界面

打开 Animator 窗口（**Window** -> **Animation** -> **Animator**），你会看到几个主要部分：

- **Layer (图层)**：用于组织动画，可以有多个图层，每个图层可以有不同的混合模式。通常一个项目从一个 "Base Layer" 开始。
    
- **Parameters (参数)**：用于在代码中控制动画状态的变量。常见的参数类型有 **Float**（浮点数）、**Int**（整数）、**Bool**（布尔值）和 **Trigger**（触发器）。
    
- **State Machine (状态机)**：这是核心部分。它由一系列动画状态（如 "Idle"、"Run"、"Jump"）和连接它们的过渡线组成。
    

### 3. 创建动画状态和过渡

1. 添加动画片段：
    
    将你的动画文件（比如 .fbx 导入的动画或在 Unity 中创建的 .anim 文件）从 Project 窗口拖到 Animator 窗口的 State Machine 区域。每个动画文件会自动创建一个新的动画状态（方框）。
    
2. 创建过渡 (Transitions)：
    
    右键点击一个状态（比如 "Idle"），选择 Make Transition，然后点击另一个状态（比如 "Run"）。一条从 "Idle" 指向 "Run" 的箭头就会出现。
    
    选中这条箭头，在 Inspector 窗口中可以设置过渡的条件、时间和曲线。
    
3. 设置过渡条件 (Conditions)：
    
    在过渡的 Inspector 窗口中，点击 + 按钮，选择你在 Parameters 中定义的参数。例如，你可以设置条件为 "RunSpeed" > 0.1。这样，当代码中将 RunSpeed 参数值设置为大于 0.1 时，动画就会从 "Idle" 过渡到 "Run"。
    
4. 设置默认状态 (Default State)：
    
    右键点击一个状态（通常是 "Idle"），选择 Set as Layer Default State。这个状态会变成橙色，表示它是动画播放的初始状态。
    

### 4. 从代码中控制 Animator

你可以通过脚本来控制 Animator 中的参数，从而驱动动画状态的切换。



```C#
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    private Animator anim;

    void Start()
    {
        // 获取附加在同一个GameObject上的Animator组件
        anim = GetComponent<Animator>();
    }

    void Update()
    {
        // 假设通过输入获取移动速度
        float speed = Input.GetAxis("Horizontal");

        // 设置Animator中的Float参数，以控制Run动画
        // 这里的"Speed"是你在Animator的Parameters窗口中创建的参数名
        anim.SetFloat("Speed", Mathf.Abs(speed));

        // 假设按下空格键跳跃
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 设置Animator中的Trigger参数，以触发Jump动画
            // 这里的"Jump"是你在Animator的Parameters窗口中创建的参数名
            anim.SetTrigger("Jump");
        }
    }
}
```

### 5. 常用方法和技巧

- **Any State**：这是一个特殊的黄色状态，可以从**任何**其他状态过渡到它连接的状态。常用于突然发生的动画，比如受伤、死亡或跳跃。
    
- **Sub-State Machine (子状态机)**：右键点击 State Machine 区域 -> **Create Sub-State Machine**。这可以帮助你组织复杂的动画逻辑，比如把所有攻击动画都放在一个子状态机中。
    
- **Blend Tree (混合树)**：右键点击 State Machine 区域 -> **Create State** -> **From New Blend Tree**。混合树允许你根据一个或多个参数的值来平滑混合多个动画。这对于走路/跑步动画特别有用，可以根据速度参数平滑过渡。
    

这是 Unity Animator 的基础框架。通过熟练掌握这些，你可以创建出非常丰富和流畅的角色动画。