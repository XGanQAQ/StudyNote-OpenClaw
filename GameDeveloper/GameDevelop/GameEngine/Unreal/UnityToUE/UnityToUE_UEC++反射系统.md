
## UE C++ 反射三件套：UCLASS / UPROPERTY / UFUNCTION

### 概览：为什么需要反射？

C++ 没有内置反射。编译后类型信息几乎全部丢失（只有 RTTI 的 `type_info` 极其有限）。UE 需要反射来实现：

- 编辑器属性面板
- 网络复制
- 蓝图可视化脚本
- 垃圾回收
- 序列化

Unity C# 天然拥有反射（CLR/IL 元数据），而 UE 必须自己构建一套反射系统。

---

### 1. UPROPERTY — 比 [SerializeField] 强大得多

| 能力 | Unity `[SerializeField]` | UE `UPROPERTY()` |
|---|---|---|
| 序列化 | ✅ | ✅ |
| 编辑器显示 | 控制 visible/hide | `EditAnywhere`/`VisibleAnywhere`/`EditDefaultsOnly`/`EditInstanceOnly` |
| 网络复制 | ❌ 手写 RPC | `Replicated` / `ReplicatedUsing` — 变化时自动调用回调 |
| 内存管理 | 不需要（CLR GC） | `Transient`— 不序列化，仅运行时缓存 |
| 配置系统 | ❌ | `Config` — 从 ini 文件读写 |
| 蓝图访问 | ❌ | `BlueprintReadWrite` / `BlueprintReadOnly` |
| 分类 | ❌ | `Category = "My"` 编辑器分组 |

**Lyra 示例** (`LyraPawnExtensionComponent.h:98-99`)：

```cpp
UPROPERTY(EditInstanceOnly, ReplicatedUsing = OnRep_PawnData, Category = "Lyra|Pawn")
TObjectPtr<const ULyraPawnData> PawnData;

UPROPERTY(Transient)
TObjectPtr<ULyraAbilitySystemComponent> AbilitySystemComponent;
```

这 1 行 `UPROPERTY` 自动生成了：编辑器显示、网络复制、GC 追踪。在 Unity 中这三个能力要分别手动实现。

---

### 2. UFUNCTION — 比普通方法多很多能力

| 能力 | Unity | UE `UFUNCTION()` |
|---|---|---|
| 蓝图可调用 | ❌ | `BlueprintCallable` |
| 蓝图可覆写 | `virtual` | `BlueprintNativeEvent` / `BlueprintImplementableEvent` |
| 网络 RPC | `[Command]` / `[ClientRpc]` | `Client` / `Server` / `NetMulticast` / `Reliable` / `Unreliable` |
| 属性变化回调 | 手写 | `UFUNCTION()` 配合 `ReplicatedUsing` |
| 输入绑定 | `InputSystem` callback | `UFUNCTION()` 直接绑定 |

**Lyra 示例** (`LyraCharacter.h`)：

```cpp
// 蓝图可调用
UFUNCTION(BlueprintCallable, Category = "Lyra|Character")
ALyraPlayerController* GetLyraPlayerController() const;

// 蓝图中可覆写（C++ 没有实现，纯蓝图实现）
UFUNCTION(BlueprintImplementableEvent, meta=(DisplayName="OnDeathFinished"))
void K2_OnDeathFinished();

// 网络多播 RPC
UFUNCTION(NetMulticast, unreliable)
void FastSharedReplication(const FSharedRepMovement& SharedRepMovement);

// 属性复制变化回调（必须标记 UFUNCTION）
UFUNCTION()
void OnRep_PawnData();
```

---

### 3. UCLASS — 类的元数据

```cpp
// LyraPawnExtensionComponent.h:26-27
UCLASS(MinimalAPI)
class ULyraPawnExtensionComponent : public UPawnComponent, public IGameFrameworkInitStateInterface
{
    GENERATED_BODY()
    ...
};
```

| UCLASS 参数 | Unity 对应 | 说明 |
|---|---|---|
| `Blueprintable` | — | 允许从这个类创建蓝图子类 |
| `BlueprintType` | — | 可作为蓝图变量类型 |
| `Config = Game` | — | 从 ini 文件读取配置 |
| `Within = XX` | — | 只能作为 XX 类型的子对象 |
| `HideCategories` | — | 隐藏继承来的某些编辑器分类 |
| `MinimalAPI` | — | 仅导出类型本身，不导出所有 API |

---

### 4. UObject 继承体系

```
Unity:                             UE:
object                              UObject
  └─ MonoBehaviour                  └─ UActorComponent      ← LyraPawnExtensionComponent
      └─ 你的脚本                        └─ UPawnComponent
                                     └─ AActor              ← ALyraCharacter
                                     └─ UDataAsset          ← ULyraExperienceDefinition
                                     └─ UGameInstance
                                     └─ APlayerController
                                     └─ UAbilitySystemComponent
```

**关键差异**：
- UE 的 **UObject** 自带 GC（类似 Unity 但无需 `new`，必须用 `NewObject<T>()` 或 `CreateDefaultSubobject<T>()` 创建）
- UE 的 **AActor** **必须** `SpawnActor()` 创建，不能直接 `new`
- UE 的 **UActorComponent** 在构造函数中用 `CreateDefaultSubobject<T>()` 创建（Unity 是 `AddComponent`）

---

### 5. 生命周期对照

| Unity | UE |
|---|---|
| `Awake()` | `PostInitializeComponents()` 或 `OnRegister()` |
| `Start()` | `BeginPlay()` |
| `Update()` | `Tick(float DeltaTime)` — 需要 `PrimaryActorTick.bCanEverTick = true` |
| `OnDestroy()` | `EndPlay()` / `Destroy()` |
| `OnEnable()` / `OnDisable()` | `SetActorHiddenInGame()` / `SetActorEnableCollision()` |
| `Instantiate(prefab)` | `GetWorld()->SpawnActorDeferred<AActor>()` |
| `GetComponent<T>()` | `FindComponentByClass<T>()` |
| `Destroy(obj)` | `obj->Destroy()`（AActor）或 `obj->ConditionalBeginDestroy()`（UObject）|

---

### 6. UE 指针类型速查

| 类型 | 含义 | Unity 类似 |
|---|---|---|
| `TObjectPtr<T>` | UObject 智能指针，自动 GC 追踪 | 普通引用（Unity 自动管理） |
| `TSoftObjectPtr<T>` | 软引用 — 不加载资源，只有路径 | `AssetReference` |
| `TSoftClassPtr<T>` | 软引用 — 指向类而非对象 | `AssetReference` with type filter |
| `TSubclassOf<T>` | 类型安全的类引用 | 无直接对应（`typeof(T)` 但携带约束）|
| `TWeakObjectPtr<T>` | 弱引用，不阻止 GC | `WeakReference` |
| `TStrongObjectPtr<T>` | 强引用，阻止 GC | 普通引用（Unity 自动管理） |

---

### 7. GENERATED_BODY() — UE 的魔法

每当你写 `UCLASS`/`USTRUCT`/`UENUM`，**必须**加 `GENERATED_BODY()`。它提供：

- `StaticClass()` — 反射获取类型（≈ `typeof(T)`）
- `Cast<T>(obj)` — 类型安全的向下转换（≈ `obj as T`）
- `IsA<T>(obj)` — 类型检查（≈ `obj is T`）
- 网络复制枚举 — `ENetFields_Private` 所有 Replicated 属性的索引

---

### 8. 构造函数模式

Unity：
```csharp
public class MyComponent : MonoBehaviour
{
    public int health = 100;
    void Awake() { ... }
}
```

UE：
```cpp
// LyraPawnExtensionComponent.h:33
ULyraPawnExtensionComponent(const FObjectInitializer& ObjectInitializer);
```

注意：
- UE 构造函数的参数是 `FObjectInitializer&`，**不能**在这里做需要 World 的事情
- `BeginPlay()` 才是 Unity 的 `Start()`
- **不要在构造函数中调用依赖 World 的函数**（GetWorld、SpawnActor 等）

创建组件必须在构造函数中用 `CreateDefaultSubobject<T>()`：
```cpp
ALyraCharacter::ALyraCharacter(const FObjectInitializer& OI) : Super(OI)
{
    PawnExtComponent = CreateDefaultSubobject<ULyraPawnExtensionComponent>(TEXT("PawnExtension"));
    HealthComponent = CreateDefaultSubobject<ULyraHealthComponent>(TEXT("Health"));
    CameraComponent = CreateDefaultSubobject<ULyraCameraComponent>(TEXT("Camera"));
}
```

---

### 9. 开发习惯速查

| Unity | UE |
|---|---|
| `[RequireComponent(typeof(X))]` | 构造函数 `CreateDefaultSubobject<X>()` |
| `[AddComponentMenu("...")]` | `UCLASS(meta=(BlueprintSpawnableComponent))` |
| `[ExecuteInEditMode]` | `bTickInEditor = true` + `UCLASS(AutoExpandRefs)` |
| `[DisallowMultipleComponent]` | 默认不允许重复 |
| `#if UNITY_EDITOR` | `#if WITH_EDITOR` |
| `[ContextMenu("...")]` | `UFUNCTION(CallInEditor)` |
| `[Tooltip("...")]` | `UPROPERTY(meta=(Tooltip="..."))` |
