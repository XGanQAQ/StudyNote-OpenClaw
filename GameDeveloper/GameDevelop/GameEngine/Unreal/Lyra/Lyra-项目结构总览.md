
## Lyra Sample Game 项目结构总览

> UE 5.6 官方示例项目，基于 LyraStarterGame

---

### 根目录结构

| 目录 | 用途 | Unity 对应 |
|---|---|---|
| `Source/` | C++ 源代码 | `Assets/Scripts/` |
| `Content/` | 资源文件（uasset/umap）| `Assets/` |
| `Config/` | 配置文件（ini） | `Project Settings` |
| `Plugins/` | 插件 | `Packages/` |
| `Platforms/` | 平台特定配置 | `Platform Settings` |
| `Build/` | 构建脚本 | `BuildSettings` |
| `LyraStarterGame.uproject` | 项目描述文件 | `.sln` + `ProjectSettings.asset` |

---

### Source/ 目录 — C++ 代码

#### Target 文件（根目录）

| 文件 | 功能 |
|---|---|
| `LyraGame.Target.cs` | 默认游戏目标 |
| `LyraEditor.Target.cs` | 编辑器目标 |
| `LyraClient.Target.cs` | 纯客户端目标 |
| `LyraServer.Target.cs` | 纯服务器目标 |
| `*EOS*.cs` / `*Steam*.cs` | 带网络服务的变体 |

类似 Unity 的 Build Profiles，但区分了客户端/服务器目标。

#### LyraGame 模块 (`Source/LyraGame/`) — 主游戏代码

| 子目录 | 文件名示例 | 对应 Unity 概念 |
|---|---|---|
| `Character/` | `LyraCharacter.h/.cpp` | `CharacterController` + `PlayerInput` |
| `AbilitySystem/` | `LyraGameplayAbility` 等 | **无对应**（GAS 是 UE 独有的系统） |
| `Input/` | `LyraInputComponent` | `InputActionAsset` |
| `Camera/` | `LyraCameraMode_ThirdPerson` | `Cinemachine` |
| `Equipment/` | `LyraEquipmentDefinition` | 武器/装备系统 |
| `Weapons/` | `LyraGameplayAbility_RangedWeapon` | 武器逻辑 |
| `GameModes/` | `LyraGameMode` + `LyraExperienceDefinition` | `GameMode` |
| `UI/` | `LyraHUD` / `LyraWidget` | `UGUI` 脚本 |
| `Inventory/` | `LyraInventoryItemDefinition` | 背包系统 |
| `Teams/` | `LyraTeamSubsystem` | 队伍系统 |
| `Cosmetics/` | `LyraCharacterPartTypes` | 外观定制 |
| `Animation/` | `LyraAnimInstance` | `Animator` 脚本 |
| `System/` | `LyraAssetManager` | 资源管理 |
| `Player/` | `LyraPlayerController` / `LyraPlayerState` | `PlayerController` |
| `GameFeatures/` | `GameFeatureAction_*` | 模块化功能系统 |
| `Interaction/` | `LyraGameplayAbility_Interact` | 交互系统 |
| `Feedback/` | 伤害数字、上下文特效 | 反馈系统 |
| `Settings/` | 游戏设置 | `Settings` |
| `Audio/` | `LyraAudioMixEffectsSubsystem` | 音频系统 |
| `Physics/` | 物理材质、碰撞通道 | `Physics Material` |
| `Tests/` | 测试工具 | 测试 |
| `Development/` | 作弊、开发者工具 | Cheats |

#### LyraEditor 模块 (`Source/LyraEditor/`) — 编辑器工具

| 文件 | 作用 | Unity 对应 |
|---|---|---|
| `LyraEditorEngine` | 编辑器引擎初始化 | `EditorApplication` |
| `Commandlets/` | 内容验证 | `AssetPostprocessor` |
| `Validation/` | 数据校验规则 | `AssetPostprocessor.OnPreprocessAsset` |

---

### Content/ 目录 — 资源文件

| 目录 | 内容 | Unity 对应 |
|---|---|---|
| `Characters/` | 角色蓝图、Cosmetics | `Prefabs/Characters` |
| `Cameras/` | 摄像机模式 | `Cinemachine` 预设 |
| `Input/` | `IA_*` 输入动作 + `IMC_*` 映射上下文 | `InputActionAsset` |
| `GameplayEffects/` | `GE_*` 游戏效果 | 无 |
| `Weapons/` | 武器蓝图（Rifle/Pistol/Shotgun） | 武器 Prefab |
| `UI/` | Widget 蓝图 | UGUI Prefab |
| `System/Experiences/` | Experience 定义 | GameMode 数据资产 |
| `System/Teams/` | 队伍配置 | 队伍数据 |
| `Environments/` | 关卡环境 | 场景资源 |
| `Effects/` | Niagara 粒子系统 | VFX Graph |
| `Audio/` | MetaSounds | 音频资源 |
| `Feedback/` | 摄像机震动 | CameraShake |
| `PhysicsMaterials/` | 物理材质 | Physics Material 2D/3D |

---

### Config/ 目录 — 配置文件

| 文件 | 作用 | Unity 对应 |
|---|---|---|
| `DefaultEngine.ini` | 引擎设置（渲染/物理/网络） | `Project Settings` |
| `DefaultGame.ini` | 游戏设置 | `GameManager` 配置 |
| `DefaultInput.ini` | 输入映射 | `Input System` 配置文件 |
| `DefaultGameplayTags.ini` | GameplayTags 定义 | **无** |
| `DefaultScalability.ini` | 不同硬件等级缩放 | Quality Settings |
| `DefaultDeviceProfiles.ini` | 设备配置文件 | 设备适配 |
| `Windows/`、`Android/` 等 | 平台特定覆盖 | Platform Settings |

---

### Plugins/ 目录 — 插件

| 插件 | 类型 | 作用 |
|---|---|---|
| **ShooterCore** | GameFeature | 射击核心功能 |
| **ShooterMaps** | GameFeature | 射击关卡地图 |
| **ShooterExplorer** | GameFeature | 探索模式 |
| **ShooterTests** | GameFeature | 自动化测试 |
| **TopDownArena** | GameFeature | 俯视角竞技场模式 |
| **AsyncMixin** | 运行时 | 异步加载混合 |
| **CommonGame** | 运行时 | 通用游戏框架 |
| **CommonUser** | 运行时 | 用户/登录系统 |
| **CommonLoadingScreen** | 运行时 | 加载画面 |
| **GameSettings** | 运行时 | 设置系统 |
| **GameSubtitles** | 运行时 | 字幕 |
| **GameplayMessageRouter** | 运行时 | 游戏消息路由 |
| **ModularGameplayActors** | 运行时 | 模块化 Actor |
| **PocketWorlds** | 运行时 | 口袋世界（小地图等）|
| **UIExtension** | 运行时 | UI 扩展系统 |
| **LyraExampleContent** | 内容 | 示例资源 |

Unity 类比：GameFeature 插件 ≈ Unity 的 **Feature Set**（按需加载的游戏功能包），普通插件 ≈ **自定义 Package**。

---

### 核心架构设计模式

#### 1. Game Feature 系统

```
GameMode (轻量)
  └── ExperienceDefinition (数据资产 - UPrimaryDataAsset)
        ├── GameFeaturesToEnable → 启用哪些 GameFeature 插件
        ├── DefaultPawnData      → 用什么角色
        ├── Actions[]            → 加载时要做什么
        │     ├── GameFeatureAction_AddAbilities
        │     ├── GameFeatureAction_AddInputBinding
        │     ├── GameFeatureAction_AddWidget
        │     └── GameFeatureAction_AddGameplayCue
        └── ActionSets[]         → 组合其他 Action 集合
```

相当于：**一个 ScriptableObject 配置整个游戏模式及其依赖的所有子系统**。

#### 2. Modular Character 设计

```
ALyraCharacter (AModularCharacter)
  ├── ULyraPawnExtensionComponent  ← 初始化协调器
  ├── ULyraHealthComponent         ← 血量逻辑
  ├── ULyraCameraComponent         ← 摄像机逻辑
  └── ... (ULyraAbilitySystemComponent 在 PlayerState 上)
```

UE 推荐**组合而非继承**：功能通过 `UActorComponent` 添加，而不是深层次类继承。

#### 3. 初始化状态机

`IGameFrameworkInitStateInterface` 定义了组件的初始化顺序：
```
Spawned → DataAvailable → DataInitialized → GameplayReady
```
每个阶段依赖前一个阶段，组件之间可以有严格的初始化依赖关系。

---

### 常用插件速查（来自 .uproject）

| 插件 | 用途 | Unity 对应 |
|---|---|---|
| `GameplayAbilities` | GAS 能力系统 | 无 |
| `EnhancedInput` | 增强输入系统 | Input System Package |
| `CommonUI` | 通用 UI 框架 | UGUI |
| `GameFeatures` | 游戏功能插件 | Feature Set |
| `ModularGameplay` | 模块化游戏框架 | 无 |
| `Niagara` | 粒子系统 | VFX Graph |
| `Water` | 水体系统 | 无 |
| `Metasound` | 音频系统 | 音频系统 |
| `ReplicationGraph` | 网络复制优化 | 无 |
| `SignificanceManager` | LOD 管理 | LOD Group |
| `OnlineSubsystemEOS` | Epic 在线服务 | Unity Gaming Services |
| `DataRegistry` | 数据注册表 | ScriptableObject 管理器 |
