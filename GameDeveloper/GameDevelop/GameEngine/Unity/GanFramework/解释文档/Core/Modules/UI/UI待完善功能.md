
- ESC按键可以关闭最上方的UI
- 采用的MVP架构


## MVP架构相关

让Presenter自动绑定到对应的Viewer (自动注入Viewer)

- 让UIManager可以自动注册所有的Viewer
	- 所有的Viewer的基类为ViewerBase
- Presenter目前采用独立对象的模式
	- 感觉过于臃肿麻烦
		- 我需要独立创建一个场景对象在UI目录下放，并且绑定到对应的Viewer
	- 我希望修改为，Presenter同样放在Model对象上
		- 好处
			- 结构统一，只有游戏对象 和 显示对象 2个物体
			- 方便Presenter通过游戏对象获得组件引用，从而修改Model数据
				- 目前是采用事件总线的方式传递Model引用从而让Presenter修改（感觉比较麻烦）
		- 坏处
			- Presenter 无法直接通过序列化连接UI对象
				- 该如何处理？

### Model Prensenter Viewer 之间该如何通信

核心思想：相互解耦、简单直接