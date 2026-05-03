## 一、PhysX 是什么

**PhysX** 是 **NVIDIA** 开发的一个 **实时物理引擎（Physics Engine）**，专门用于游戏和交互式应用中的物理模拟。它能让开发者在游戏里实现：

- 物体的刚体运动（Rigidbody Dynamics）
    
- 碰撞检测与碰撞反应
    
- 布料模拟（Cloth Simulation）
    
- 粒子系统（Particles）
    
- 角色控制（Character Controller）
    
- 关节与约束（Joints & Constraints）
    

简单来说，**PhysX 是一个负责“物理计算”的底层库**，Unity、Unreal 等引擎都把它作为默认物理引擎使用过（不过 Unreal 从 UE4.26 开始逐渐转向 Chaos 自研引擎，Unity 则依旧使用 PhysX 作为主要 3D 物理解决方案）。

---

## 二、PhysX 的特点

1. **跨平台**
    
    - 支持 Windows、Linux、主机（PS/Xbox/Switch）、移动端。
        
2. **高性能**
    
    - 支持多线程计算。
        
    - 可以利用 GPU 加速（CUDA）。
        
3. **模块化设计**
    
    - 刚体、碰撞检测、布料、流体等独立模块。
        
4. **游戏引擎集成度高**
    
    - Unity、Unreal 都内置了 PhysX，开发者几乎不用关心底层。
        

---

## 三、PhysX 在 Unity 里的地位

在 Unity 中，绝大多数 3D 物理系统（Collider、Rigidbody、Joint、Raycast 等）背后都由 **PhysX 负责实际计算**。

- 你在 Unity 脚本里写 `rigidbody.AddForce()`，实际上就是把指令传递给 **PhysX 引擎**，让它在下一帧物理模拟里处理。
    
- Unity 只是提供了封装和接口，让你方便使用。
    

---

## 四、类比理解

- 游戏引擎里的 **渲染** → 交给 **渲染管线（如 DirectX、Vulkan、Metal）**。
    
- 游戏引擎里的 **物理** → 交给 **PhysX**（或 Havok、Bullet、Chaos 这种物理引擎）。
    

所以：  
👉 **PhysX 就像是“物理计算的显卡驱动”**，不是 Unity 独有的东西，而是一个通用的第三方库。
