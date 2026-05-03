## 概述
DataPipeline 数据管线 是为了方便解决从策划案的配置文件数据（excel）到游戏内运行时实际能读取到的正确对应数据的问题。

职责：Excel配置转换 和 游戏存档/数据保存等，涉及序列化和反序列化的问题

**配置读取**
Excel → (Luban配表工具) → JSON → SO → (运行时读取)  Runtime

以玩家武器数据为例，分**三层结构**

> 玩家武器数据 =「静态配置」+「玩家状态」+「存档表示」

```
WeaponConfig   ← 设计时配置（策划）
        ↑
        │ 引用
WeaponRuntime    ← 运行时实例（战斗用）
        ↓
        │ 序列化
WeaponSaveData   ← 存档数据（JSON / 二进制）

```

## 进度
- 配置读取
	- [x] Excel转换Json ✅ 2026-02-10
		- [x] Luban接入 ✅ 2026-02-10
		- [x] Luban的Unity编辑器界面 ✅ 2026-02-10
	- [ ] Json转SO
	- [ ] Data与Config统一解析器（OdinSerilizer）

Json转SO遇到困难
- Json转SO无法正确注入
- Luban生成的Json的类型，如果是enum需要额外设置
- Luban的序列化器和Persistence的序列化器不一样（Netosoft和odin）
可以考虑不使用SO作为Config配置，每个类使用Json读取配置
**考虑制作一个SO基类，可以自动加载Json?**

## 基础预设功能
- Luban配表工具
	- 路径配置
	- 选择解析的SO内容文件
- 工具
	- 面板
		- 验证Excel文件是否格式规范
	- 日志

### 使用/预设规范

1. 根据Luban规范创建好表格
2. 编辑器内运行Luban，生成Json和自动生成的表格容器C#
3. 检查是否生成Json和C#
4. 编辑器内运行Json转SO文件工具
	1. 指定Json文件夹位置
	2. 指定需要转换的SO类型
	3. 指定生成的SO文件存放的位置
5. 检查是否生成SO

#### 配置读取功能

随版本发布、不热更新的配置
> 比如：武器表、技能表、怪物表（你现在阶段很常见）

- Json
	- Assets/GameData/Configs/Json/
- ScriptableObject
	- Assets/GameData/Configs/SO/xxx(对应Json文件的名称)/
- Code 自动生成的C#代码
	- Assets/Scripts/Auto/ConfigsData
- Excel文件存储的位置
	- Assets/GameData/Datas/
- 生成的c#容器类
	- Assets/Scripts/Gameplay/Auto/

可热更新 / 可服务器下发的配置
```
Application.persistentDataPath/
 └── Config/
     └── weapons.json
```

## 依赖工具
- **UniTask**
	- 异步加载、任务系统支持
- Odin Serializer
	- 数据序列化与反射支持
	- 奥丁序列化工具，提供更多可序列化类型
	- 为了解决Unity 原生的序列化器对 C# 类型的支持非常有限
- **Newtonsoft.Json**
	- JSON 解析与调试输出
- Luban
	- 进行Excel文件转换到Json的读取
	- 并进行代码生成

## 实现设计

## 参考

- [finkkk/Fink-Framework: Fink Framework是由Fink个人开发的供unity使用的轻量游戏框架。该框架提供了完整数据管线、对象池、事件系统、资源加载系统等诸多常用功能。](https://github.com/finkkk/Fink-Framework)
- [数据管线概述（Overview） - Fink Framework使用文档](https://finkkk.cn/docs/fink-framework/data-pipeline/data-overview)
- [Luban](Luban.md)
