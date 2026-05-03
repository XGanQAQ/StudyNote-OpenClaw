## 概述
Persisten-持久化功能 是为了方便解决游戏持久化数据保存的问题

职责：游戏存档/数据保存等，涉及序列化和反序列化的问题

**存档读取**
JSON → 反序列化 →Runtime → 序列化 → JSON

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

## 基础预设功能
- 持久化数据
	- Odin-JSON格式保存
		- 将游戏运行中的数据持久化保存为JSON格式文件
	- Odin-JSON格式读取
		- 游戏运行时读取保存的JSON注入到实例当中
- 工具
	- 面板
	- 日志

### 使用/预设规范

#### 存档文件

以Json格式保存读取数据  
Json文件保存在 Application.persistentDataPath 当中  

**以类为基础**
保存的数据类必须带有SaveKey标签  
Json文件的名称为SaveKey标签设置的名称

**类中部分字段保存**
类的成员标签
带有`SaveMember`的成员会被识别保存
## 依赖工具
- **UniTask**
	- 异步加载、任务系统支持
- Odin Serializer
	- 数据序列化与反射支持
	- 奥丁序列化工具，提供更多可序列化类型
	- 为了解决Unity 原生的序列化器对 C# 类型的支持非常有限
- **Newtonsoft.Json**
	- JSON 解析与调试输出

## 实现设计

## 参考

- [finkkk/Fink-Framework: Fink Framework是由Fink个人开发的供unity使用的轻量游戏框架。该框架提供了完整数据管线、对象池、事件系统、资源加载系统等诸多常用功能。](https://github.com/finkkk/Fink-Framework)
- [数据管线概述（Overview） - Fink Framework使用文档](https://finkkk.cn/docs/fink-framework/data-pipeline/data-overview)
- [Luban](Luban.md)
