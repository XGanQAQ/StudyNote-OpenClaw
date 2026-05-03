这是我对于git-amend发布的如何编写事件总线视频其中最终的事件总线代码的解读
## 教程视频/源代码
源代码仓库： [adammyhre/Unity-Event-Bus](https://github.com/adammyhre/Unity-Event-Bus#)

【【Unity】学习构建高级事件总线：Unity架构实践】 https://www.bilibili.com/video/BV1FNyZB3ENw/?share_source=copy_web&vd_source=445f9fe806d1b40f2620f76957091c99

[Learn to Build an Advanced Event Bus | Unity Architecture](https://www.youtube.com/watch?v=4_DTAnigmaQ)

## 如何使用的例子
```cs
public struct PlayerEvent : IEvent {
    public int health;
    public int mana;
}

EventBinding<PlayerEvent> playerEventBinding;

void OnEnable() {    
    playerEventBinding = new EventBinding<PlayerEvent>(HandlePlayerEvent);
    EventBus<PlayerEvent>.Register(playerEventBinding);

    // Can Add or Remove Actions to/from the EventBinding
}

void OnDisable() {
    EventBus<PlayerEvent>.Deregister(playerEventBinding);
}

void Start() {
    EventBus<PlayerEvent>.Raise(new PlayerEvent {
        health = healthComponent.GetHealth(),
        mana = manaComponent.GetMana()
    });    
}

void HandlePlayerEvent(PlayerEvent playerEvent) {
    Debug.Log($"Player event received! Health: {playerEvent.health}, Mana: {playerEvent.mana}");
}
```

## 架构原理
通过泛型系统，构建一个完善的事件总线框架

- IEvent
	- 所有具体自定义事件类型继承此接口
- IEventBinding
	- EventBinding
		- 用于将函数绑定到事件
- EventBus
	- 提供用于注册、注销和触发自定义事件的静态函数
- EventBusUtil
	- 用于 EventBus 的 静态初始化方法和其他实用程序
- PredefineAssemblyUtil
	-  用于定位程序集并查找其中类型的 实用类

### EventBus的基本运行原理
EventBinding和EventBus都为泛型，且泛型约束为继承了IEvent接口的类。

**通过不同的泛型类型参数来指明其对应的总线类型**
每一个继承了IEvent接口的具体Event实现，都会有一个其对应的事件总线。

IEventBinding封装了无参事件和有参事件，通过其泛型`<T>`来指定此事件绑定器对应的事件类型。

EventBus为泛型静态类，其中有集合用来存储所有的IEventBinding。

一个EventBinding可以添加多个方法回调
一个EventBus可以添加多个EventBinding
（他们的泛型`<T>`是相同的）
这样在Raise一种Event类型的时候，所有此类型的EventBinding都会被激活，触发其中的回调。
在取消注册一个EventBinding的时候，只有对应的回调不再触发。

### EventBusUtil是如果找到所有的EventBus的？
1. 静态泛型类是可以根据你调用的时候的不同T来生成不同的静态类的。
2. `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]` EventBusUtil给Initialize方法添加了此Attribute特性来实现在场景调用之前加载此静态方法
3. 通过`PredefineAssemblyUtil`查询到所有程序集中继承了IEvent的类型
4. 先获得开放式泛型的Type对象，然后遍历上面获得的IEvent类型，调用`typedef.MakeGenericType`来构造出具体的类型
	1. 它使用反射 (Reflection) 的 MakeGenericType 方法，将当前的 eventType (例如 PlayerMoveEvent) 填充到开放式泛型 EventBus<> 中，动态地生成了一个具体的 EventBus 类型。
5. 然后存储到具体的列表中

其实`EventBus<T>`不在这里被构造，但是在别的地方被调用，也可以直接使用。只不过这里是为了将所有的事件总线存储在了一起，方便后续添加更多相关工具方法。

### PredefineAssemblyUtil是如何定位程序集并查找其中类型的？
`PredefinedAssemblyUtil` 旨在从应用程序域中所有已加载的程序集里，**仅筛选出 Unity 预定义的四个程序集**（`Assembly-CSharp`, `Assembly-CSharp-Editor`, `Assembly-CSharp-firstpass`, `Assembly-CSharp-Editor-firstpass`）。

**它定位和查找类型分为两步：**

1. **程序集定位：** 通过程序集名称进行**精确字符串匹配**，将非预定义的程序集（包括所有**自定义程序集**）排除在外。
    
2. **类型查找：** 尽管筛选了四个，但最终只检查 **`Assembly-CSharp`** 和 **`Assembly-CSharp-firstpass`** 这两个运行时程序集中的所有类型，找出实现了给定接口的类并返回。

该工具类**不能**读取或处理自定义程序集中的类型。

