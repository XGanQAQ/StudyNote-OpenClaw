### 主题目标  
理解 **为什么 Release 错一次就会出问题**

# Addressables 的引用计数机制

## 核心机制
- 每次 Load 增加引用计数
- 每次 Release 减少引用计数
- 计数归零 → 资源可卸载

## 常见问题
- 多次 Load 少 Release → 内存泄漏
- 少 Load 多 Release → 崩溃或异常

## 设计原则
谁 Load，谁 Release