# 资源加载概述

本章节介绍 **ResLoad 资源加载系统** 的整体设计理念、目标与核心结构。  
ResLoad 是 Fink Framework 内置的统一资源加载模块，基于 **Provider 插件系统 + 引用计数 + 缓存管理** 实现，适用于中小型到中大型 Unity 项目。

ResLoad 提供了对 Resources、本地文件、网络资源、编辑器资源 等多种来源的统一加载能力，是整个框架资源体系的基础。

---

## 1. 设计目标

原生 Unity 加载（Resources / AssetBundle 等）存在以下问题：

- 缺乏统一的加载入口
- 无引用计数，易造成重复加载和内存浪费
- 异步加载无法合并回调，逻辑复杂
- 错误路径加载不易定位
- 无法自由扩展新的加载方式
- 缺乏全局调试、缓存可视化能力

为解决上述问题，ResLoad 系统的设计目标包括：

- **统一的加载入口**（一套 API 加载所有资源来源）
- **可扩展的 Provider 插件架构**（Resources / File / Web / Editor / AB）
- **自动缓存与引用计数管理**
- **同步、异步（await）、回调、句柄（支持进度）多种加载方式**
- **标准化卸载策略与资源生命周期控制**
- **可调试、可追踪、可扩展，适配未来热更 / AB / Addressables**

---

## 2. 核心组成模块

ResLoad 由以下几个关键结构构成：

### **2.1 ResManager**

资源加载调度中心，负责：

- 路径解析、前缀路由
- Provider 选择
- 缓存管理
- 引用计数
- 同步 / 异步加载封装
- 卸载策略
- 批量加载
- 异常恢复（任务丢失托底机制）

### **2.2 ResInfo<`T`>**

资源状态记录结构，包含：

- 已加载的资源实例
- 异步任务（task）
- 引用计数（refCount）
- 卸载标记（isDel）

用于 ResManager 对资源生命周期进行统一管理。

### **2.3 Provider（资源提供器）**

定义资源的实际加载方式，例如：

- ResourcesProvider
- FileProvider
- WebProvider
- EditorProvider

未来可扩展：

- AssetBundleProvider
- AddressablesProvider
- 任何自定义数据源

所有 Provider 都必须实现 `IResProvider` 接口，形成插件式架构。

### **2.4 ResOperation / BatchOperation**

用于异步加载的句柄对象，支持：

- 加载进度
- 完成事件
- 不使用 async/await 的场景
- 多资源批量加载

---

## 3. 路径系统

ResLoad 通过前缀（prefix）来决定资源的加载方式：

|前缀|Provider|示例|
|---|---|---|
|`res://`|ResourcesProvider|`res://UI/Login`|
|`file://`|FileProvider|`file:///C:/Data/icon.png`|
|`http://` / `https://`|WebProvider|`https://server.com/a.png`|
|`editor://`|EditorProvider（仅编辑器）|`editor://UI/Icon`|

无前缀时默认使用 `ResourcesProvider`。

同时 ResLoad 会自动执行：

- 路径标准化（统一 `/` 分隔符）
- 禁止 `://` 或 `:` 开头等非法格式
- 拼接唯一资源键值：  
    fullPath + "_" + typeof(T).Name

---

## 4. 为什么需要 ResLoad

相较于 Unity 原生加载方式，ResLoad 带来以下优势：

**资源生命周期可控** 引用计数结合缓存，使得资源何时加载、何时卸载变得明确可控。

**避免重复加载与内存浪费** 相同资源只加载一次，同步与异步共享缓存。

**插件式加载 自由拓展** Provider 架构允许轻松接入任何加载源，并且自由拓展。例如：本地文件、网络资源、AB 热更包、Addressables、自定义数据源等。