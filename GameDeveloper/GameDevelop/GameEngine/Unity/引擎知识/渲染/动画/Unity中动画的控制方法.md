在 Unity 里，**Animator/动画的控制方法**主要分为几大类：

---

## ① **Animator 组件常用 API**

这是最直接的方式，通过 `Animator` 脚本接口操作：

- **播放控制**
    
    - `SetTrigger(string name)`：触发一个 **Trigger 参数**，常用于切换状态机动画。
        
    - `ResetTrigger(string name)`：重置 Trigger。
        
    - `SetBool(string name, bool value)` / `GetBool(string name)`
        
    - `SetInteger(string name, int value)` / `GetInteger(string name)`
        
    - `SetFloat(string name, float value)` / `GetFloat(string name)`  
        👉 用来驱动 Animator Controller 的参数，从而触发状态机切换。
        
- **直接播放动画片段**
    
    - `Play(string stateName, int layer = -1, float normalizedTime = float.NegativeInfinity)`  
        👉 不走状态机过渡，直接播放指定动画状态。
        
    - `CrossFade(string stateName, float transitionDuration, int layer = -1, float normalizedTime = float.NegativeInfinity)`  
        👉 在一段时间内平滑过渡到指定动画。
        
- **状态信息获取**
    
    - `GetCurrentAnimatorStateInfo(int layerIndex)` → `AnimatorStateInfo`
        
    - `GetNextAnimatorStateInfo(int layerIndex)`  
        👉 可以判断当前播放的动画名称、是否循环、播放进度（`normalizedTime` 0~1）。
        
- **动画速度与层权重**
    
    - `animator.speed` → 控制整个 Animator 播放速度。
        
    - `GetLayerWeight(int layerIndex)` / `SetLayerWeight(int layerIndex, float weight)`  
        👉 控制多层动画（比如上半身与下半身分层）。
        

---

## ② **通过 Animation Clip 控制（传统 Animation 组件）**

如果不是 `Animator` 而是 **旧版 `Animation` 组件**：

- `animation.Play("Run")`
    
- `animation.CrossFade("Walk")`
    
- `animation["Run"].speed = 2.0f;`  
    👉 这种方式现在主要用于简单动画或 Legacy 项目。
    

---

## ③ **使用 `AnimatorOverrideController` 动态替换动画**

- 可以在运行时 **替换 Animator Controller 中某些动画片段**：
    
    ```csharp
    AnimatorOverrideController aoc = new AnimatorOverrideController(animator.runtimeAnimatorController);
    aoc["Idle"] = newIdleClip;
    animator.runtimeAnimatorController = aoc;
    ```
    
    👉 常用于角色换装、技能动画替换。
    

---

## ④ **Playable API（可编程动画系统）**

Unity 提供了 **PlayableGraph**，更底层、可编程：

- `AnimationClipPlayable`：直接播放动画片段。
    
- `AnimatorControllerPlayable`：驱动 Animator Controller。
    
- `AnimationMixerPlayable`：混合多个动画。
    
- `AnimationLayerMixerPlayable`：多层混合。
    

这种方式适合需要 **高度动态组合动画** 的场景，比如技能系统、Procedural 动画。

---

## ⑤ **Timeline / Signal 驱动**

如果是过场动画或复杂演出，可以用 **Timeline** 来控制 Animator：

- 可以在 Timeline 里插入动画轨道，脚本里调用 `PlayableDirector.Play()` 来播放。
    
- 也可以用 `Signal` 来触发事件。
    

---

## ⑥ **OnAnimatorXXX 回调**

Animator 也会提供一些事件回调：

- `OnAnimatorMove()` → 接管动画的 Root Motion。
    
- `OnAnimatorIK(int layerIndex)` → 处理 IK。
    
- `OnStateEnter/OnStateUpdate/OnStateExit`（需要继承 `StateMachineBehaviour` 脚本）→ 在状态切换时执行逻辑。
    

---

## ⑦ **动画事件（Animation Event）**

在 Animation Clip 上添加 **事件回调点**：

- 在某一帧调用脚本函数。
    
- 常用于攻击判定、音效触发。
    

---

✅ **总结一下**：  
Unity 动画的脚本操作主要有

- **Animator API**（参数、Play、CrossFade、Layer、StateInfo）
    
- **AnimatorOverrideController**（动态替换动画）
    
- **Playable API**（可编程控制、混合）
    
- **Timeline 驱动**
    
- **回调（OnAnimatorMove/OnAnimatorIK/StateMachineBehaviour）**
    
- **动画事件**
    
- （旧版）Animation API
    

---

要不要我帮你整理一份 **“Animator 控制全流程常用代码速查表”**？这样你写脚本时可以直接查用。