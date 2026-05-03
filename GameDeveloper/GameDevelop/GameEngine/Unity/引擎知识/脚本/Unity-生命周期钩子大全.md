Unity 的“生命周期钩子”分为 **运行时（Player）** 与 **编辑器（Editor）** 两大类。  
下面给出一张 **“一图胜千言”式速查表**，按 **调用顺序** 与 **使用场景** 整理，复制即可当小抄。

--------------------------------------------------
一、运行时（Runtime）（Build 与 Play Mode 都会走）
--------------------------------------------------
| 阶段 | 钩子 | 典型用途 |
|---|---|---|
| **脚本实例刚刚诞生** | `Awake()` | 初始化自身数据、组件缓存；不依赖外部顺序。 |
| **脚本启用瞬间** | `OnEnable()` | 注册事件、开启协程、重置状态；每次 `SetActive(true)` 都会进。 |
| **首次 Update 之前** | `Start()` | 依赖别人先 `Awake` 时用；可安全访问外部组件。 |
| **物理步**（固定间隔） | `FixedUpdate()` | 刚体加力、物理计算；默认 0.02 s 一次。 |
| **内部物理步结束** | `FixedUpdate()` 之后 | 物理查询 (`Physics.Raycast` 等) 最稳时机。 |
| **动画/状态机更新** | `OnAnimatorMove()` | 自定义根运动 (Root Motion)。 |
| **碰撞/触发进入** | `OnCollisionEnter` / `OnTriggerEnter` | 碰撞逻辑入口。 |
| **碰撞/触发持续** | `OnCollisionStay` / `OnTriggerStay` | 持续伤害、摩擦。 |
| **碰撞/触发离开** | `OnCollisionExit` / `OnTriggerExit` | 清理状态。 |
| **帧更新** | `Update()` | 输入、非物理移动、每帧逻辑。 |
| **晚于所有 Update** | `LateUpdate()` | 相机跟随、UI 对齐；保证别人先动。 |
| **渲染前** | `OnPreRender()` / `OnWillRenderObject()` | 自定义裁剪、替换 Pass。 |
| **渲染后** | `OnPostRender()` | 画调试线、截图。 |
| **脚本禁用** | `OnDisable()` | 反注册事件、停止协程；每次 `SetActive(false)` 都会进。 |
| **脚本销毁** | `OnDestroy()` | 释放资源、清理静态引用。 |
| **程序退出** | `OnApplicationQuit()` | 存档、释放网络连接。 |
| **暂停/恢复** | `OnApplicationPause(bool)` | 移动端来电/切后台。 |
| **聚焦/失焦** | `OnApplicationFocus(bool)` | 暂停音乐、拉通知。 |

--------------------------------------------------
二、编辑器（Editor-Only）—— Build 后不会调用
--------------------------------------------------
| 钩子 | 说明 |
|---|---|
| `Reset()` | 首次添加组件或 Reset 菜单时；用于给字段填默认值。 |
| `OnValidate()` | Inspector 里每次改字段立即触发；检查范围、自动补引用。 |
| `OnDrawGizmos()` / `OnDrawGizmosSelected()` | 场景视图画调试形、图标。 |
| `OnSceneGUI()`（继承 `Editor` 类） | 自定义场景视图交互手柄。 |

--------------------------------------------------
三、 ScriptableObject 也有生命周期
--------------------------------------------------
| 钩子 | 说明 |
|---|---|
| `Awake()` | 创建实例后调用（含资源加载）。 |
| `OnEnable()` | 每次资源被加载 / inspector 选中触发。 |
| `OnDisable()` | 资源被卸载时。 |
| `OnDestroy()` | 从内存移除时。 |

--------------------------------------------------
四、速记口诀（背下来即可）
--------------------------------------------------
“**Awake 先缓存，Start 再依赖；Fixed 做物理，Update 处理输入；Late 做相机，OnEnable/Disable 管注册；OnDestroy 清引用，OnApplication 管退出。**”