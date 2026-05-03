- Model
	- 纯C#
	- 游戏数据
- Viewer
	- 游戏对象 GameObject
	- 界面UI
	- 一切可见
- Presenter
	- 纯C#
- Installer
	- **负责“创建 + 连接 + 启动” MVP 对象，但不参与任何业务逻辑**

View 是演员  
Presenter 是导演  
Model 是剧本  
Installer 是“开机时把人都叫到片场的副导演”

## 总结

> **在 MVP 中：  
> UI 是 View，角色是 View，建筑是 View，  
> 只要它“被看见、被操作、依赖 Unity”，它就是 View。**

而：

> **Model 是“世界规则的抽象”，不是“世界的物体本身”。**


## QA