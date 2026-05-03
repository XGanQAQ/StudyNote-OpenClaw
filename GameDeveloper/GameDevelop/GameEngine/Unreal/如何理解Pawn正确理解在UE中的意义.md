在虚幻引擎中，**Pawn (棋子/兵卒)** 是一个非常核心的概念，它代表了**可以被控制器（Controller）拥有的所有Actor（对象）**。

您可以将其理解为Unity中**可以被玩家或AI控制的“游戏角色”**，但虚幻引擎中的“Pawn”概念更广义一些。

### Pawn 的核心特征：

1. **可被控制器拥有 (Possessable by Controllers)**：这是Pawn最显著的特征。Pawn本身并不具备控制逻辑，它只是一个**载体**。它需要被一个`Controller`（控制器，可以是玩家控制器`PlayerController`或AI控制器`AIController`）“拥有”（Possess），才能被驱动。
2. **通常具备移动能力**：Pawn通常会有一个`MovementComponent`（比如`PawnMovementComponent`或更常用的`CharacterMovementComponent`），使其能够在世界中移动。
3. **输入接收者**：当一个Pawn被控制器拥有后，它可以接收来自该控制器的输入（例如玩家的键盘/鼠标/手柄输入，或者AI的决策指令）。

### Pawn 与其他相关类的关系：

- **Actor**：
    - `Actor`是虚幻引擎中所有对象的基类，是可放置在世界中的任何东西。
    - **所有Pawn都是Actor**，但不是所有Actor都是Pawn。
    - **类比Unity：** `GameObject`是Unity中所有对象的基类。所有可以被控制的角色（例如您的Player GameObject）本质上都是`GameObject`。
- **Character (角色)**：
    - `Character`是`Pawn`的子类。它是为**人形或类似人形**的角色专门设计的。
    - `Character`默认带有一个**`CharacterMovementComponent`**（角色移动组件），这个组件提供了更高级的移动功能，如行走、跑步、跳跃、跌落、攀爬等，并且内置了网络同步功能。
    - **当您需要一个可以行走、跳跃的玩家或AI角色时，通常会使用`Character`而不是直接使用`Pawn`。**
    - **类比Unity：** 想象一个`GameObject`上挂载了`CharacterController`或一个复杂的自定义移动脚本。`Character`可以被认为是虚幻引擎提供的一个“预制”的，更完善的，用于实现这种移动逻辑的`Pawn`。
- **Controller (控制器)**：
    - `Controller`是负责**拥有并控制**`Pawn`的Actor。它本身是不可见的，在场景中没有物理表现。
    - 有两种主要类型的`Controller`：
        - **`PlayerController` (玩家控制器)**：接收玩家的输入，并将其转化为对所拥有Pawn的控制。一个玩家通常对应一个`PlayerController`。
        - **`AIController` (AI控制器)**：负责AI的决策逻辑，并控制AI所拥有的Pawn。
    - **类比Unity：** Unity中没有一个完全对应的独立类。您通常会将玩家输入处理脚本直接放在Player `GameObject`上，或者AI的决策逻辑也放在AI `GameObject`上。而在虚幻引擎中，**控制逻辑和被控制对象是分离的**。这个分离是虚幻引擎设计哲学的一个重要体现，它使得多人游戏和AI的实现更加清晰和模块化。

### 为什么Pawn和Controller要分离？

这种分离是虚幻引擎的强大之处，尤其体现在：

1. **多人游戏 (Multiplayer)**：
    - 在多人游戏中，`PlayerController`可以在服务器和客户端之间复制，而`Pawn`也可以独立于`Controller`进行复制。
    - 当一个玩家断开连接并重新连接时，可以很方便地将他们原有的`PlayerController`重新“拥有”一个新的`Pawn`，或者在玩家死亡后，`PlayerController`可以“抛弃”当前的`Pawn`并“拥有”一个新的`Pawn`（比如重生）。
    - 在服务器端，`PlayerController`持续存在，即使玩家的Pawn被销毁。这使得服务器可以跟踪玩家的状态和数据，而不需要Pawn一直存在。
2. **AI 系统**：
    - AI逻辑（在`AIController`中）可以独立于具体的AI角色模型（在`Pawn`中）进行设计。您可以为不同种类的AI角色使用相同的AI行为树，只需要切换它们所拥有的`Pawn`即可。
3. **解耦与模块化**：
    - 将“如何控制”与“被控制的对象”分离，使得系统更加模块化，便于维护和扩展。
    - 例如，您可以为同一个Pawn编写不同的控制器（一个玩家控制器，一个AI控制器）。或者，同一个控制器可以用于控制不同的Pawn（比如一个机器人控制器可以控制一个飞行Pawn，也可以控制一个陆地Pawn）。

### 简单总结：

- **Pawn**：**可以被玩家或AI控制的、在世界中存在的“对象”（通常是角色或载具）。** 它只是一个容器，不包含控制逻辑。
- **Controller**：**负责驱动Pawn的“大脑”，接收输入并做出决策。** 它本身不可见。
- **Character**：Pawn的子类，专为人形或类似人形角色设计，具有更高级的移动能力。
