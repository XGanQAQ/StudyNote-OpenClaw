# C++ 与 C# 结构体和类的区别对比

## 对比表

| 特性 | C++ | C# |
|------|-----|-----|
| struct 默认访问 | public | private |
| class 默认访问 | private | private |
| struct 继承 | ✅ 支持 | ❌ 不支持 |
| class 继承 | ✅ 支持 | ✅ 支持 |
| struct 无参构造 | ✅ 可定义 | ❌ 不能显式定义 |
| 默认值 | 未定义（需手动初始化） | 自动初始化为默认值 |
| 空值支持 | 不能为 null | struct 不能 null, class 可以 |
| 垃圾回收 | 手动管理 | GC 自动管理 |

## 核心差异

C++ 中 struct 和 class **几乎是等价的**，唯一区别是默认访问权限。  
C# 中 struct 和 class 有**本质区别**：struct 是值类型、不支持继承、不能 null。
