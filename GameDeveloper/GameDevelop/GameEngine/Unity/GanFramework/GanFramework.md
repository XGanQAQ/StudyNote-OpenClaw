个人总结的游戏开发框架，方便快速开发，不涉及Gameplay逻辑
根据过去项目经验，总结出游戏开发框架。
需要将其转换为那种可以用Github直接导入的形式，方便导入

## 待做

- [x] 倒计时工具 ✅ 2026-01-02
- [x] 数据导入保存管线 [Persisten-持久化功能](Persisten-持久化功能.md) ✅ 2026-01-02
- [x] 优化UI框架 ✅ 2026-02-21
- [x] 资源管理 ✅ 2026-02-21
- [x] 小规模重构 ✅ 2026-03-13
	- [x] Foundation 层（绝对底层） ✅ 2026-03-13
	- [x] Infrastructure 层（基础设施层） ✅ 2026-03-13
	- [x] Feature 层（业务层） ✅ 2026-03-13
- [ ] Framework 启动架构：无需在场景内挂载对象进行基本单例管理器初始化
- [ ] Log框架(优先级较低，Unity本身的日志系统即可使用)
- [ ] 通用作弊面板，通过反射和标签来调用方法，方便调试
- [ ] 通用配置读取单例，方便读取配置信息，结合luban
- [ ] 模块文档
	- [x] 事件总线 ✅ 2026-03-13
	- [x] 数据持久化 ✅ 2026-03-13
	- [ ] 设计模式
	- [x] 资源加载 ✅ 2026-03-13
	- [ ] 配置管线
### 目标：

**轻量级框架**：最小可用、可扩展、不 over-design、不包含具体Gameplay逻辑
框架的目的是为了提高效率，将过去重复的代码提炼出来，作为基础。并且规范开发的流程和项目架构。

框架分为3个部分
- 工具 Utils
	- 一些在开发Gameplay过程中实用的工具
	- 包括拓展方法、实用脚本、常见的Gameplay脚本
- 核心 Core
	- 核心运行脚本，不涉及具体Gameplay逻辑，包含游戏开发场景的需求
	- 核心编辑器工具，和核心脚本配套的工具
- 约定
	- 约定的游戏开发流程，在此流程下，可以保证核心的正常运行，且高效的工作

关于插件：
可以采纳实用的任在更新的插件

关于安装：
我希望这个框架能有一个极为方便的启动方法
- 直接引入一个包，即可使用大量框架中的实用工具
- 一个包为游戏核心
	- 核心脚本
	- 核心编辑器
- 准备Unity自定义项目模板，在生成的时候准备好文件夹分类
	- 约定部分

### 核心特性

- [Utils 实用工具库](Utils%20实用工具库.md)
- [入门场景管理-多场景加载架构](入门场景管理-多场景加载架构.md)
- [依赖管理-分层混合依赖管理方案](依赖管理-分层混合依赖管理方案.md)
- UI管理-逻辑与显示分离
- 事件总线

- GanFramework
	- EventBus 事件总线.
		- 跨模块
		- 多个不确定的监听者
		- 避免单例滥
	- UI
		- 事件总线驱动
		- 类MVP模式
			- 逻辑与显示的分离
		- 自动锁定/解锁鼠标
	- ResLoad 资源管理
		- 统一资源获取入口
		- 支持 Resource Addressable File 等多种获取途径
	- Patterns 设计模式
		- 基础常用的设计模式基类
	- Data 数据系统
		- 可支持多种序列化方法
		- 通过接入Odin Serializer 实现数据保存加载
			- 并支持Unity对象的引用自动解析
	- Config配置系统
		- 通过接入Luban 实现从Excel到Json文件，并自动生成对应的C#类

### 外部依赖插件
- Unity
	- InputSystem
	- TextMeshPro
	- UGUI
	- Addressable
- 插件
	- Unitask
		- 源码导入
		- 异步工具
	- Odin Serializer
		- 源码导入
		- 序列化
	- Newtonsoft
		- 源码导入
		- Json转换
	- ExcelDataReader
		- Excel读取
	- Luban
		- Luban 工具
			- 工具DLL
		- com.code-philosophy.luban
			- Luban自动生成数据类必要的依赖
			- https://gitee.com/focus-creative-games/luban_unity.git

### 相关笔记
[架构说明](架构说明.md)

### 参考资料

[新人分享：Unity入门之后如何进阶——游戏框架_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1emndznE4Y/?spm_id_from=333.337.search-card.all.click&vd_source=1015af2504b4c9c5deda584505666669)
![](Pasted%20image%2020251012141732.png)

[[Unity24届]《黎明深渊》类巫师ARPG Demo 个人求职作品_游戏热门视频](https://www.bilibili.com/video/BV1hw4m1f7MU/?spm_id_from=333.788.comment.all.click&vd_source=1015af2504b4c9c5deda584505666669)
[HalfADog/Unity-ARPGGameDemo-TheDawnAbyss: This is an ARPG game Demo that mimics the Witcher III.](https://github.com/HalfADog/Unity-ARPGGameDemo-TheDawnAbyss)

[Alex-Rachel/TEngine: Unity框架解决方案-支持HybridCLR(最好的次时代热更)、Obfuz混淆代码加固与YooAssets(优秀商业级资源框架)。](https://github.com/Alex-Rachel/TEngine/tree/main)

[Fink Framework —— 适用于 Unity 的轻量游戏开发框架 - 元界](https://finkkk.cn/archives/37f5c545-ac86-4398-85a7-ecb0791574c1)