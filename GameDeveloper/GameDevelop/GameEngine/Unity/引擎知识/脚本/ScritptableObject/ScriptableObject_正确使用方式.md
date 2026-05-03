# ScriptableObject 的正确使用方式

## 核心思想
ScriptableObject 只做「模板」，不做「实例」

## 错误示例
直接用 SO 存玩家当前武器数据

## 正确分层结构

- WeaponConfigSO（静态配置）
- WeaponSaveData（存档数据）
- WeaponRuntimeData（运行时状态）

## 设计原则
- SO 不参与逻辑状态变化
- SO 可被多个对象共享
