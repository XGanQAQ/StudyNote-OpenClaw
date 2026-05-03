# 为什么需要 Addressables

## Unity 默认资源加载的问题
- Scene 引用即加载
- 引用了就常驻
- 卸载时机不透明
- 资源耦合严重

## 常见后果
- 场景切换内存不降
- Prefab / SO 常驻内存
- 引用链不可控

## Addressables 的意义
把资源“从 Scene 中解放出来”
