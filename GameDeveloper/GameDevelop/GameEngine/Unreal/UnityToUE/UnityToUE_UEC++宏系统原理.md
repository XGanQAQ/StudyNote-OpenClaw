
## UE C++ 宏系统原理：从定义到运行时

UE 的宏系统是整个引擎的基石。与 Unity C# 的运行时反射不同，UE 用**编译时代码生成**在 C++ 中实现了完整的反射系统。

---

### 整体架构：四层管线

```
┌──────────────────────────────────────────────────────────────────┐
│  第一层: 宏定义 (ObjectMacros.h)                                  │
│  对 C++ 编译器"撒谎"：大部分宏展开为空，仅作为标记                │
│  部分宏展开为 token 粘贴，连接生成文件名与行号                    │
├──────────────────────────────────────────────────────────────────┤
│  第二层: 代码生成器 (UHT — UnrealHeaderTool)                     │
│  独立的 C# 程序，编译前运行                                       │
│  解析 .h 文件中的 UCLASS/UPROPERTY/UFUNCTION 标记                │
│  输出 .generated.h + .gen.cpp                                    │
├──────────────────────────────────────────────────────────────────┤
│  第三层: 生成的 C++ 代码                                          │
│  .generated.h → GENERATED_BODY() 展开为真正的 C++ 代码            │
│  .gen.cpp     → 反射数据 + 自注册函数                            │
├──────────────────────────────────────────────────────────────────┤
│  第四层: 运行时                                                   │
│  DLL 加载 → 静态对象 FRegisterCompiledInInfo                     │
│          → ConstructUClass() 创建 UClass 对象                    │
│          → 注册 Property/Function/Interface                      │
│          此时 StaticClass() 才真正可用                            │
└──────────────────────────────────────────────────────────────────┘
```

---

### 第一层：宏定义 — 这些宏到底是什么？

**UPROPERTY/UFUNCTION 等是空宏**（`ObjectMacros.h`）：

```cpp
// 官方注释：这些宏只被 UHT 解析，C++ 编译时被忽略
#define UPROPERTY(...)        // ← 完全展开为空
#define UFUNCTION(...)        // ← 完全展开为空
#define USTRUCT(...)          // ← 完全展开为空
#define UENUM(...)            // ← 完全展开为空
```

**UCLASS 用 token 粘贴**生成唯一标识符：

```cpp
#define UCLASS(...) BODY_MACRO_COMBINE(CURRENT_FILE_ID,_,__LINE__,_PROLOG)

#define BODY_MACRO_COMBINE(A,B,C,D) A##B##C##D
```

例如，`LyraCharacter.h:97` 的 `UCLASS()` 展开为：
```
FID_Dev_..._LyraCharacter_h_97_PROLOG
```

这个标识符在 `.generated.h` 中被**再次定义**为具体代码。

**GENERATED_BODY 同样用 token 粘贴**：

```cpp
#define GENERATED_BODY(...) BODY_MACRO_COMBINE(CURRENT_FILE_ID,_,__LINE__,_GENERATED_BODY);
```

展开为：
```
FID_Dev_..._LyraCharacter_h_100_GENERATED_BODY;   // 注意结尾有分号
```

---

### 第二层：UHT — 核心解析器

UHT（UnrealHeaderTool）是一个 **C# 写的独立程序**，构建流水线的一部分。

**工作步骤：**

1. **读取所有 .h 文件**
   - 寻找 `UCLASS(`、`UPROPERTY(`、`UFUNCTION(`、`GENERATED_BODY(` 等模式
   - 它的 C++ 解析能力有限——只关心这些宏标记

2. **构建类型图**
   - 谁继承谁（如 `ULyraPawnExtensionComponent` → `UPawnComponent`）
   - 类有什么属性（name, type, flags, offset）
   - 类有什么函数（name, params, flags）
   - 类实现了什么接口

3. **计算网络复制索引**
   - 为每个 `UPROPERTY(Replicated)` 分配枚举值：
   ```cpp
   // LyraPawnExtensionComponent.generated.h:43-47
   enum class ENetFields_Private : uint16 {
       NETFIELD_REP_START = (uint16)((int32)Super::ENetFields_Private::NETFIELD_REP_END + 1),
       PawnData = NETFIELD_REP_START,
       NETFIELD_REP_END = PawnData
   };
   ```

4. **生成 .generated.h**
   - 定义上述所有 token 标识符为实际代码块
   - 包含 `DECLARE_FUNCTION`、`DECLARE_CLASS2` 等

5. **生成 .gen.cpp**
   - 属性描述符结构体
   - 函数描述符结构体
   - 注册函数

---

### 第三层：生成的代码

#### .generated.h 内容

`GENERATED_BODY()` 展开为 (`LyraPawnExtensionComponent.generated.h:62-69`)：

```cpp
#define FID_..._LyraPawnExtensionComponent_h_29_GENERATED_BODY \
PRAGMA_DISABLE_DEPRECATION_WARNINGS \
public:
    // ↓ UFUNCTION 的 thunk 函数声明
    FID_..._RPC_WRAPPERS_NO_PURE_DECLS \
    // ↓ StaticClass(), 复制枚举, 序列化器
    FID_..._INCLASS_NO_PURE_DECLS \
    // ↓ 删除拷贝构造, vtable helper
    FID_..._ENHANCED_CONSTRUCTORS \
private: \
PRAGMA_ENABLE_DEPRECATION_WARNINGS
```

**RPC_WRAPPERS** 展开为 (`LyraPawnExtensionComponent.generated.h:24-27`)：

```cpp
#define RPC_WRAPPERS \
    DECLARE_FUNCTION(execOnRep_PawnData); \
    DECLARE_FUNCTION(execGetLyraAbilitySystemComponent); \
    DECLARE_FUNCTION(execFindPawnExtensionComponent);
```

其中 `DECLARE_FUNCTION` 定义在 `ObjectMacros.h:761`：

```cpp
// 每个 UFUNCTION 生成一个"thunk"函数
#define DECLARE_FUNCTION(func) \
    static void func(UObject* Context, FFrame& Stack, RESULT_DECL)
```

Thunk 函数是蓝图 VM 调用 C++ 的桥梁——它从 `FFrame& Stack` 中解析参数，压入返回值。

**INCLASS_NO_PURE_DECLS** 展开为：

```cpp
#define INCLASS_NO_PURE_DECLS \
    DECLARE_CLASS2(ULyraPawnExtensionComponent, UPawnComponent,
                   COMPILED_IN_FLAGS(0 | CLASS_Config),
                   CASTCLASS_None,
                   TEXT("/Script/LyraGame"),
                   Z_Construct_UClass_ULyraPawnExtensionComponent_NoRegister) \
    DECLARE_SERIALIZER(ULyraPawnExtensionComponent) \
    ...
```

`DECLARE_CLASS2` 展开为 (`ObjectMacros.h:1797-1841`)：

```cpp
#define DECLARE_CLASS2(TClass, TSuperClass, TStaticFlags, ...) \
    typedef TSuperClass Super;       // ← 定义基类别名
    typedef TClass ThisClass;        // ← 定义自身别名
    // ← 就是这行实现 StaticClass()
    inline static UClass* StaticClass() {
        return GetPrivateStaticClass();
    }
    static constexpr EClassFlags StaticClassFlags = ...;
    // 自定义 new 操作符 — 必须用 UE 的内存分配
    inline void* operator new(size_t InSize, EInternal, ...) {
        return StaticAllocateObject(StaticClass(), ...);
    }
```

#### .gen.cpp 内容

**`FObjectPropertyParams`** 结构体描述一个 `UPROPERTY` 的所有元信息：

```cpp
// LyraPawnExtensionComponent.gen.cpp:257
const UECodeGen_Private::FObjectPropertyParams
NewProp_PawnData = {
    "PawnData",                              // 属性名
    "OnRep_PawnData",                        // RepNotify 回调函数名
    (EPropertyFlags)0x0124080100000821,      // 属性标志
    EPropertyGenFlags::Object | EPropertyGenFlags::ObjectPtr,
    RF_Public|RF_Transient|RF_MarkAsNative,  // 对象标志
    nullptr, nullptr, 1,
    STRUCT_OFFSET(ULyraPawnExtensionComponent, PawnData),  // ← 编译期成员偏移量！
    Z_Construct_UClass_ULyraPawnData_NoRegister,           // 类型引用
    METADATA_PARAMS(...)                      // 编辑器元数据
};
```

**`STRUCT_OFFSET`** 是关键 (`UnrealTemplate.h:220-224`)：

```cpp
#ifdef __clang__
#define STRUCT_OFFSET(struc, member) __builtin_offsetof(struc, member)
#else
#define STRUCT_OFFSET(struc, member) offsetof(struc, member)  // 标准 C++
#endif
```

这让运行时能用**编译期计算出的偏移量**直接访问属性，完全不需要字符串查找。

**接口描述** (`LyraPawnExtensionComponent.gen.cpp:269-271`)：

```cpp
const FImplementedInterfaceParams InterfaceParams[] = {
    { Z_Construct_UClass_UGameFrameworkInitStateInterface_NoRegister,
      (int32)VTABLE_OFFSET(ULyraPawnExtensionComponent, IGameFrameworkInitStateInterface),
      false },
};
```

虚函数表偏移量也是编译期计算的！

**重头戏 — `Z_Construct_UClass_*` 工厂函数** (`LyraPawnExtensionComponent.gen.cpp:176-199`)：

```cpp
UClass* ULyraPawnExtensionComponent::GetPrivateStaticClass() {
    if (!Z_Registration_Info.Singleton) {
        GetPrivateStaticClassBody(
            StaticPackage(),                    // 包名 "/Script/LyraGame"
            TEXT("ULyraPawnExtensionComponent"),// 类名
            Singleton,
            StaticRegisterNativesULyraPawnExtensionComponent,  // 注册 native 函数
            sizeof(TClass),                     // 对象大小
            alignof(TClass),                    // 对齐
            ClassFlags,                         // EClassFlags
            CastFlags,                          // EClassCastFlags
            ConfigName,                         // Config = Game
            Constructor,                        // 构造函数指针
            VTableHelperCtorCaller,
            StaticFunctions,
            &Super::StaticClass,                // 父类 UClass
            &WithinClass::StaticClass           // Outer 类型
        );
    }
    return Singleton;
}
```

---

### 第四层：运行时 — DLL 加载自注册

`.gen.cpp:309-318` 底部的全局对象：

```cpp
struct Z_CompiledInDeferFile_..._Statics {
    static constexpr FClassRegisterCompiledInInfo ClassInfo[] = {
        { Z_Construct_UClass_ULyraPawnExtensionComponent,     // 构造器
          ULyraPawnExtensionComponent::StaticClass,           // StaticClass
          TEXT("ULyraPawnExtensionComponent"),
          &Z_Registration_Info_UClass_ULyraPawnExtensionComponent,
          CONSTRUCT_RELOAD_VERSION_INFO(sizeof(TClass), CRC) }
    };
};

// ↓ 全局静态对象！DLL 加载时构造函数自动执行
static FRegisterCompiledInInfo Z_CompiledInDefer_...(
    TEXT("/Script/LyraGame"),
    ClassInfo, nullptr, 0, nullptr, 0);
```

**加载时序：**

```
DLL 被操作系统加载
  → 全局静态对象 Z_CompiledInDefer_... 的构造函数执行
  → 引擎收到注册请求
  → ...稍后...
  → 引擎调用 Z_Construct_UClass_ULyraPawnExtensionComponent()
  → 内部调用 GetPrivateStaticClassBody()
  → 再调用 ConstructUClass(UClass*&, const FClassParams&)
  → 在 ConstructUClass 中：
    1. 创建 UClass* 对象
    2. 将所有 FObjectPropertyParams → UProperty
    3. 将所有 FFunctionParams → UFunction
    4. 注册接口
    5. 设置父类（Super::StaticClass()）
  → 现在 StaticClass() 返回有效的 UClass*
  → 编辑器才能显示属性面板，网络系统才能复制
```

---

### 总结：一句话说清楚本质

```
Unity C#: [SerializeField] → IL 元数据 → 运行时 GetCustomAttribute()
UE C++:   UPROPERTY()     → UHT 生成 C++ 代码 → DLL 加载时 ConstructUClass()
```

| 维度 | Unity C# | UE C++ |
|---|---|---|
| **实现方式** | CLR 内置 IL 元数据 | UHT 代码生成 + 运行时注册 |
| **是否需要标记** | 不需要（可反射任意类型） | **必须**标记 UCLASS/UPROPERTY |
| **性能** | 字符串查找 + JIT | 偏移量 + 函数指针直接调用 |
| **网络复制** | 手动写 RPC | `Replicated` 自动 |
| **蓝图支持** | 无原生支持 | 反射数据直接暴露给蓝图 VM |
| **GC** | CLR 自动 | UE 自己的 `AddReferencedObjects` |
| **第三方库** | 可直接反射 | 不能（除非标记） |

### 关键的宏总结

| 宏 | 真实展开 | 作用 |
|---|---|---|
| `UPROPERTY(...)` | 空 | 仅给 UHT 看 |
| `UFUNCTION(...)` | 空 | 仅给 UHT 看 |
| `UCLASS(...)` | token 粘贴 → `CURRENT_FILE_ID`_`__LINE__`_PROLOG | 给 .generated.h 做锚点 |
| `GENERATED_BODY()` | token 粘贴 → 完整的类基础设施 | StaticClass、Super、复制枚举等 |
| `DECLARE_FUNCTION(func)` | `static void func(UObject*, FFrame&, RESULT_DECL)` | 蓝图 thunk 函数声明 |
| `DECLARE_CLASS2(...)` | StaticClass、Super 别名、operator new | 类注册的 C++ 侧代码 |
| `STRUCT_OFFSET` | `offsetof()` | 编译期计算成员偏移量 |
