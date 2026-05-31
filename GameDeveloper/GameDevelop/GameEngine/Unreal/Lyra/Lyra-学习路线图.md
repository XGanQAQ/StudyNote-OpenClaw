
## 从 Unity 转 UE 学习路线图

> 基于 Lyra Sample Game 项目，以 Lyra 为参考的渐进式学习路径

---

### 阶段 1：UE C++ 基础与反射系统

**目标**：理解 UE 独特的 C++ 编程范式

- [[UnityToUE_UEC++反射系统]] — UCLASS/UPROPERTY/UFUNCTION
- [[UnityToUE_UEC++宏系统原理]] — 宏从定义到运行时的完整流程
- UObject 生命周期与 GC
- `NewObject<T>()` vs `SpawnActor<T>()`
- 智能指针：`TObjectPtr` / `TSoftObjectPtr` / `TSubclassOf` / `TWeakObjectPtr`
- `Cast<T>()` vs Unity 的 `as T`
- `TArray` / `TMap` / `TSet` vs `List<T>` / `Dictionary<T,K>` / `HashSet<T>`

**Lyra 参考**：`Source/LyraGame/LyraGame.Build.cs` 模块结构，`LyraAssetManager.h` 中的模板模式

**产出**：能读懂 Lyra 中任何 .h 文件的类声明

---

### 阶段 2：Actor 与 Component 系统

**目标**：理解 UE 的 Actor/Component 架构

- `AActor` vs `GameObject`
- `UActorComponent` vs `MonoBehaviour`
- 生命周期函数：`BeginPlay()` / `Tick()` / `EndPlay()`
- 组件创建：`CreateDefaultSubobject<T>()` vs `AddComponent<T>()`
- Actor 网络复制：`bReplicates` / `SetReplicates()`
- UE 的模块化设计哲学：组合优先于继承

**Lyra 参考**：
- `Character/LyraCharacter.h` — `AModularCharacter` + 组件组合
- `Character/LyraPawnExtensionComponent.h` — 核心扩展组件
- `Character/LyraHealthComponent` — 血量组件

**练习**：在 Lyra 中添加一个自定义 `UActorComponent`

---

### 阶段 3：GameplayTags

**目标**：理解 UE 的层级标签系统（Unity Tag 的升级版）

- `FGameplayTag` vs Unity Tag（字符串 vs 层级结构）
- `FGameplayTagContainer` — 多标签集合
- 标签匹配：`HasTag()` / `HasAll()` / `HasAny()`
- 标签的父/子关系：`A.B.C` 匹配 `A.B`
- `Config/DefaultGameplayTags.ini` 定义位置
- 与 UPROPERTY 配合：`FGameplayTagQuery`

**Lyra 参考**：
- `LyraGameplayTags.h/.cpp` — 自定义标签定义
- `Source/LyraGame/` 中几乎所有地方都在用 GameplayTag

---

### 阶段 4：Enhanced Input 系统

**目标**：掌握 UE 的新输入系统

- `UInputAction`（IA_*）vs Unity Input Action
- `UInputMappingContext`（IMC_*）vs Control Scheme
- 输入优先级与上下文栈
- 输入修饰器（Modifiers）和触发器（Triggers）
- 本地玩家输入子系统
- 可重映射按键

**Lyra 参考**：
- `Content/Input/` 中的 `IA_*.uasset` 和 `IMC_Default.uasset`
- `Source/LyraGame/Input/` 全部文件
- `LyraInputComponent` / `LyraPlayerMappableKeyProfile`

---

### 阶段 5：Gameplay Ability System (GAS)

**目标**：掌握 UE 最核心、与 Unity 差异最大的系统

- `UAbilitySystemComponent`（ASC）
- `UGameplayAbility`（GA）vs 技能 CD/消耗
- `UAttributeSet`（AS）vs 角色属性
- `UGameplayEffect`（GE）vs Buff/Debuff
- `FGameplayTag` 在整个系统中充当事件/状态标识
- 游戏阶段系统

**Lyra 参考**：
- `Source/LyraGame/AbilitySystem/` 整个目录
- `Source/LyraGame/Equipment/` — 装备技能
- `Source/LyraGame/Weapons/` — 武器技能
- `Content/GameplayEffects/`
- `Content/Input/Actions/`

---

### 阶段 6：Lyra Experience 系统

**目标**：理解 Lyra 的模块化游戏模式设计

- `ULyraExperienceDefinition` + `GameFeatureAction`
- GameFeature 插件架构
- 动态加载/卸载游戏功能

**Lyra 参考**：
- `GameModes/LyraExperienceDefinition.h`
- `GameModes/LyraGameMode.h`
- `GameFeatures/GameFeatureAction_*.h`
- `Plugins/GameFeatures/` 中的 5 个插件

---

### 阶段 7：UI 框架 (Common UI / UMG)

**目标**：掌握 UE 的 UI 系统

- UMG vs UGUI
- CommonUI 框架：`UCommonButtonBase` / `UCommonListView`
- UI 扩展系统
- 输入路由与 UI

**Lyra 参考**：
- `Source/LyraGame/UI/`
- `Content/UI/`
- `Plugins/UIExtension/`
- `Plugins/CommonGame/`

---

### 推荐的学习方法

1. **读代码** — Lyra 是 Epic 官方写的最现代化的 UE 示例
2. **改代码** — 修改一个组件观察效果
3. **对照官方文档** — `Docs/` 目录下的官方指南
4. **用 Editor 理解** — 编辑器中查看 UPROPERTY 的暴露效果
5. **断点调试** — 用 Visual Studio 断点跟踪生命周期函数

---

### 关键概念映射总表

| Unity | UE (Lyra 对应) |
|---|---|
| `GameObject` + `Transform` | `AActor` + `USceneComponent` |
| `MonoBehaviour` | `UActorComponent` |
| `Start()` / `Update()` | `BeginPlay()` / `Tick()` |
| `Instantiate()` | `SpawnActorDeferred<T>()` → `FinishSpawning()` |
| `Destroy(obj)` | `obj->Destroy()` |
| `GetComponent<T>()` | `FindComponentByClass<T>()` |
| `[SerializeField]` | `UPROPERTY(EditAnywhere)` |
| `[RequireComponent]` | `CreateDefaultSubobject<T>()` 在构造函数 |
| `ScriptableObject` | `UDataAsset` / `UPrimaryDataAsset` |
| Prefab | 蓝图类 |
| Scene | Level + Sublevel |
| LayerMask | 自定义碰撞通道（Object/Trace Channels）|
| 字符串 Tag | `FGameplayTag`（层级结构）|
| Animator Controller | `UAnimBlueprint` + `UAnimInstance` |
| Animator.SetTrigger | `TryActivateAbility()` + GameplayTag |
| Coroutine / Invoke | `FTimerHandle` + `GetWorld()->GetTimerManager()` |
| Input System | Enhanced Input (IA + IMC) |
| Cinemachine | `UCameraMode` 子类 |
| Physics.Raycast | `LineTraceSingleByChannel()` |
| Resources.Load | `TSoftObjectPtr` + `AssetManager` |
| `Awake()` | `OnRegister()` / `PostInitProperties()` |
| OnCollisionEnter | `OnHit()` / `OnBeginOverlap()` |
| `#if UNITY_EDITOR` | `#if WITH_EDITOR` |
