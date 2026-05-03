| 方法                              | 是否推荐  | 典型用途                |
| ------------------------------- | ----- | ------------------- |
| `RuntimeInitializeOnLoadMethod` | ⭐⭐⭐⭐⭐ | 全局 Gameplay Service |
| 框架 Bootstrap（纯 C#）              | ⭐⭐⭐⭐⭐ | 大型项目 / 模块化          |
| Editor 扫描 + Runtime 生成          | ⭐⭐⭐⭐⭐ | 自动注册 Service        |
| ScriptableObject 驱动初始化          | ⭐⭐⭐⭐☆ | 数据驱动 Gameplay       |
| GameManager 手动 new              | ⭐⭐⭐☆☆ | 中小项目                |
| 反射扫描运行时                         | ⭐⭐☆☆☆ | 原型 / 工具             |
| 场景 Mono Awake                   | ❌     | 不符合你的目标             |