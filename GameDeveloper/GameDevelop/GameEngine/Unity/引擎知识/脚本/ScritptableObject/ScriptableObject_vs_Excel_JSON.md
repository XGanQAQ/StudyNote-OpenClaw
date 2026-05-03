# ScriptableObject 与 Excel / JSON 的关系

## 三者定位对比

| 形式 | 本质 | 主要用途 |
|----|----|----|
| Excel | 编辑工具 | 策划配置 |
| JSON | 数据载体 | 存档 / 网络 / 热更新 |
| ScriptableObject | Unity Asset | 引擎内直接使用 |

## 推荐数据流
Excel → JSON → ScriptableObject → Runtime

## 结论
ScriptableObject 不是配置源头，而是 Unity 运行时最友好的配置形态。
