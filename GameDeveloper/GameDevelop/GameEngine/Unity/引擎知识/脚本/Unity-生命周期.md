## 🌱 1. 初始化阶段

1. **Awake()**
    
    - **时机**：脚本实例被载入时调用（无论物体是否激活）。
        
    - **特点**：只调用一次；比 Start 更早。
        
    - **常用场景**：初始化引用（比如 `GetComponent`）、单例模式初始化。
        
2. **OnEnable()**
    
    - **时机**：物体或脚本启用时调用（包括首次启用或再次启用）。
        
    - **常用场景**：注册事件、启动协程。
        
3. **Start()**
    
    - **时机**：在第一次 Update 之前调用（仅当脚本启用时）。
        
    - **常用场景**：依赖于其他对象初始化的逻辑（比如 UI 初始化、玩家出生点设定）。
        

---

## 🔄 2. 游戏循环阶段

### 帧循环调用顺序（重要）

1. **FixedUpdate()**
    
    - **时机**：以固定的时间间隔调用（默认 0.02s），**和物理引擎同步**。
        
    - **常用场景**：处理物理相关逻辑（Rigidbody 移动、力的作用）。
        
2. **Update()**
    
    - **时机**：每帧调用一次。
        
    - **常用场景**：大多数逻辑（输入检测、非物理移动、计时）。
        
3. **LateUpdate()**
    
    - **时机**：在所有 Update 执行完之后调用。
        
    - **常用场景**：摄像机跟随、依赖于其他对象已经更新完成的逻辑。
        

---

## 🎮 3. 物理相关回调

- **OnTriggerEnter / OnTriggerStay / OnTriggerExit**
    
- **OnCollisionEnter / OnCollisionStay / OnCollisionExit**  
    👉 必须有 Collider，至少一个有 Rigidbody。
    

---

## 📦 4. 渲染相关回调

- **OnPreCull / OnBecameVisible / OnBecameInvisible / OnRenderObject / OnPostRender**  
    👉 一般不常考，偏向图形渲染。
    

---

## 🛑 5. 禁用 & 销毁阶段

1. **OnDisable()**
    
    - **时机**：脚本或物体禁用时调用。
        
    - **常用场景**：取消事件注册、停止协程。
        
2. **OnDestroy()**
    
    - **时机**：对象被销毁时调用（场景切换、`Destroy()`）。
        
    - **常用场景**：资源释放、反注册。
        

---

## 🧩 典型调用顺序总结

```txt
Awake()
OnEnable()
Start()
Update()
LateUpdate()
OnDisable()
OnDestroy()
```

---

## 🌟 面试小Tips

- 如果面试官问 **“Awake 和 Start 的区别”**  
    👉 Awake 用来做不依赖其他对象的初始化，Start 用来做依赖于其他对象的初始化。
    
- 如果问 **“Update 和 FixedUpdate 区别”**  
    👉 Update 每帧调用，受帧率影响；FixedUpdate 按固定间隔，和物理同步。
    
- 如果问 **“LateUpdate 用来干嘛”**  
    👉 典型场景是摄像机跟随（要等角色 Update 完才更新）。
    
