【（中文语音）Unity 输入系统必须掌握的三种简易工作流程】 https://www.bilibili.com/video/BV1MSyoBHEeZ/?share_source=copy_web&vd_source=445f9fe806d1b40f2620f76957091c99

示例里面存在大量的预制体可以使用
屏幕触控器

### 直接读取设备


## 使用输入资产 不生成C#类

使用PlayerInput组件
4种模式
- Send Messages
	- 发送事件到对应的方法
- Broadcast Messages 
	- 广播到所有的子对象
- Invoke Unity Events
	- 采用Unity编辑器事件的注册方式
- Invoke C Sharp Events
	- 发送CSharp 事件

## 生成C#类
会生成一套接口，继承此接口的方法可以被反射

> 可使用ScriptableObject 让其不依赖场景