# Unity 游戏引擎

## 生命周期
- [MonoBehaviour 生命周期图](引擎知识/脚本/Unity-生命周期流程图-monobehaviour_flowchart.md)
- [生命周期钩子大全](引擎知识/脚本/Unity-生命周期钩子大全.md)
- [生命周期实现原理](引擎知识/脚本/Unity-生命周期函数的实现原理.md)
- [Awake vs Start](常见问题/Unity-用Start还是Awake初始化.md)
- [OnValidate](引擎知识/脚本/Unity-OnValidate.md)
- [脱离 Scene 的初始化](常见问题/Unity-脱离Scene和生命周期的初始化方法有哪些.md)
- [IDisposable 的妙用](引擎知识/脚本/Unity-IDisposable的妙用.md)

## 脚本基础
- [Unity 架构](引擎知识/脚本/Unity架构.md)
- [重要的类](引擎知识/脚本/重要的类.md)
- [单例与 MonoBehaviour](引擎知识/脚本/Unity-单例是否继承MonoBehaviour.md)
- [序列化规则](个人编写记录/小技巧/unity中哪些类型可以序列化到编辑器编辑.md)
- [脚本管理技巧](个人编写记录/小技巧/如何合理的管理你的脚本程序.md)
- [单例模板](个人编写记录/小技巧/单例模板.md)

### ScriptableObject
- [什么是 ScriptableObject](引擎知识/脚本/ScritptableObject/Unity-ScriptableObject-是什么.md)
- [使用原则总结](引擎知识/脚本/ScritptableObject/ScriptableObject_使用原则总结.md)
- [正确使用方式](引擎知识/脚本/ScritptableObject/ScriptableObject_正确使用方式.md)
- [存储位置与生命周期](引擎知识/脚本/ScritptableObject/ScriptableObject_存储位置与生命周期.md)
- [与 MonoBehavior 生命周期区别](常见问题/Unity-ScriptableObject与MonoBehaviour的生命周期区别.md)
- [OnEnable/OnDisable 触发时机](常见问题/Unity-ScriptableObject-OnEnable和OnDisable生命周期事件的触发时机.md)
- [哪些配置不该用 SO](引擎知识/脚本/ScritptableObject/哪些配置不该用_SO.md)
- [ScriptableObject vs Excel/JSON](引擎知识/脚本/ScritptableObject/ScriptableObject_vs_Excel_JSON.md)
- [ScriptableObject + Addressables](引擎知识/脚本/ScritptableObject/ScriptableObject_与_Addressables.md)

### 异步编程
- [协程 vs Async vs UniTask](引擎知识/脚本/异步/Unity-IEnumerator协程-Async-Unitask.md)
- [UniTask 使用](引擎知识/脚本/异步/UniTask.md)

## 渲染
- [URP 渲染模块](引擎知识/渲染/Unity-URP-渲染相关的模块都有哪些？.md)
- [自定义渲染管线](引擎知识/渲染/自定义渲染管线.md)
- [Renderer Feature](引擎知识/渲染/Renderer%20Feature.md)
- [ShaderLab Tag](引擎知识/渲染/Shader/ShaderLab%20Tag的作用与实现原理.md)
- [渲染宏](引擎知识/渲染/Unity的渲染宏.md)
- [SRP Batcher](engine script/Unity-URP...)

### 动画
- [动画控制方法](引擎知识/渲染/动画/Unity中动画的控制方法.md)
- [Animator 基本用法](引擎知识/渲染/动画/Unity-Animator的基本用法参考.md)

### 骨骼
- [骨骼动画](引擎知识/渲染/骨骼/Unity骨骼动画相关知识.md)

## 物理系统
- [Unity Physics 总览](引擎知识/物理/Unity-Physics.md)
- [PhysX 详解](引擎知识/物理/Unity-PhysX.md)

## 多线程与高性能
- [Job System](引擎知识/多线程/Unity-JobSystem.md)
- [Burst Compiler](引擎知识/多线程/Unity-Burst.md)
- [Compute Shader](引擎知识/多线程/Unity-ComputeShader.md)
- [EOS/AOT/LLVM](引擎知识/多线程/Unity-AOT.md)
- [SIMD](引擎知识/多线程/Unity-SIMD.md)
- [Native Code](引擎知识/多线程/Unity-NativeCode.md)

## 资源加载
- [资源加载总览](引擎知识/资源加载/Unity-资源加载都有哪些？.md)
- [资源定位](引擎知识/资源加载/Unity-资源定位.md)
- [Addressables 是什么](引擎知识/资源加载/Addressables/Addressables_是什么.md)
- [Addressables 管理什么](引擎知识/资源加载/Addressables/Addressables_管理的是什么.md)
- [Addressables 引用计数](引擎知识/资源加载/Addressables/Addressables_引用计数.md)
- [Addressables 高频小资源](引擎知识/资源加载/Addressables/Addressable-高频加载小资源.md)
- [AssetReference 使用](引擎知识/资源加载/Unity-AssetReference.md)
- [打包方法](引擎知识/资源加载/Unity都有哪些打包方法.md)
- [AssetBundle 基础](个人编写记录/AssertBundle的基础用法.md)

## 性能优化
- [性能优化手段](性能优化/Unity-性能优化-都有哪些手段.md)
- [程序集加速编译](个人编写记录/小技巧/使用程序集来加速Unity的编译速度.md)

## 实用 Attribute
- [Attribute 大全](常见问题/Unity-实用标签-Attribute.md)
- [Vector3 相等性判断](常见问题/Unity-Vector3的相等性判断问题.md)

## 编辑器工具
- [TypeCache 编辑器工具](引擎知识/编辑器/Unity-TypeCache-类型扫描-编辑器工具.md)

## InputSystem
- [InputSystem 概述](引擎插件/InputSystem/InputSystem.md)
- [三种工作流程](引擎插件/InputSystem/Unity-InputSystem-输入系统必须掌握的三种简易工作流程.md)

## 常见问题
- [Excel 转游戏数据](常见问题/Unity-Excel转游戏数据问题.md)

## 个人项目记录
- [2D 染色游戏](个人编写记录/2D染色游戏/日志.md)
- [故障效果 Shader](个人编写记录/故障效果/Unity-ShaderGraph-故障效果.md)
- [溶解效果](个人编写记录/溶解效果/README.md)
- [CRT 扫描线](个人编写记录/CRT%20扫描线/CRT%20扫描线屏幕后处理-URP.md)
- [激光反射](个人编写记录/LaserAndReflection/2D横板-如何实现激光与激光反射效果.md)
- [六边形网格](个人编写记录/Hexagon/如何程序化生成六边形网格地形.md)
- [物体建造系统](个人编写记录/物体建造系统/物体建造系统.md)
- [完美 UI 制作](个人编写记录/如何制作完美的UI/HowToMakePerfectUI.md)
- [Unity + Git](个人编写记录/小技巧/使用git进行版本控制及团队协作.md)
- [服务端框架](个人编写记录/GameServer/服务端框架分析.md)
- [客户端框架](个人编写记录/GameServer/客户端框架分析.md)
- [FBX 提取 AnimationClip](个人编写记录/Unity-从FBX文件中提取AnimationClip动画.md)
- [TMP 字体替换](个人编写记录/Unity-Editor-TextMeshPro字体替换.md)
