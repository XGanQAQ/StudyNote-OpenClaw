## What is MVC
![[MVC 架构图.png]]
MVC架构中，View显示Model，Controller修改Model，User看见View，使用Controller
User通过控制器来修改Model数据，View读取Model中的数据更新来刷新显示


## What is MVP
![[MVP 架构图.png]]
MVP中，Presenter作为中间人
玩家交互链条：User通过View发出UI事件，Presenter接受到UI事件，修改Model。
数据显示更新链条：Model发出数据修改事件，Presenter接受到Model事件，更新View，User看到View的变化

## Example （Unity）

```cs
public class Health: MonoBehaviour
 {
    public event Action HealthChanged;
    private const int minHealth = 0;
    private const int maxHealth = 100;
    private int currentHealth;
    public int CurrentHealth { get => currentHealth; set => current
Health = value; }
    public int MinHealth => minHealth;
    public int MaxHealth => maxHealth;
    public void Increment(int amount)
    {
        currentHealth += amount;
        currentHealth = Mathf.Clamp(currentHealth, minHealth, max
Health);
        UpdateHealth();
    }
    public void Decrement(int amount)
    {
        currentHealth -= amount;
        currentHealth = Mathf.Clamp(currentHealth, minHealth, max
Health);
        UpdateHealth();
    }
    public void Restore()
    {
        currentHealth = maxHealth;
        UpdateHealth();
    }
    public void UpdateHealth()
    {
        HealthChanged?.Invoke();
    }
 }
```
Health类可以被视为MVP中的Model

```cs
public class HealthPresenter : MonoBehaviour
 {
    [SerializeField] Health health;
    [SerializeField] Slider healthSlider;
    private void Start()
    {
        if (health != null)
        {
            health.HealthChanged += OnHealthChanged;
        }
        UpdateView();
    }
    private void OnDestroy()
    {
        if (health != null)
        {
            health.HealthChanged -= OnHealthChanged;
        }
    }
    public void Damage(int amount)
    {
        health?.Decrement(amount);
    }
    public void Heal(int amount)
    {
        health?.Increment(amount);
    }
    public void Reset()
    {
        health?.Restore();
    }
    public void UpdateView()
    {
        if (health == null)
            return;
        if (healthSlider !=null && health.MaxHealth != 0)
        {
            healthSlider.value = (float) health.CurrentHealth / (float)
 health.MaxHealth;
        }
    }
    public void OnHealthChanged()
    {
        UpdateView();
    }
 }
```
HealthPresenter可以被视为Prensenter，其中的Slider为View。
我们可以通过调用Presenter的方法来控制Model，并且Presenter会将监听Model变化的事件，然后更新View。

## 思考
View不仅仅可以是Unity的直接组件，也可以是自己封装之后的自定义组件。但是View应该只负责显示相关的逻辑（依据传进来的数据，显示对应的效果）

MVP的职责分离优势
在Unity项目中，如此的MVP模式，将数据的更新逻辑和前端的显示分离为2个部分。这样就可以让一个人负责数据逻辑，一个人专门负责前端。

###  MVP和事件总线的结合

Presenter 应该通过什么方式监听 Model 的变化？  
——直接订阅 Model 事件？还是用事件总线？

>**如果事件只属于当前业务模块内部，就让 Presenter 直接订阅 Model 的事件。**  
>**如果事件需要跨模块传播，就让 Model 使用 EventBus 广播事件。**

🔵 **Presenter 与 Model 之间的事件：用于 UI 层局部更新，不对全局暴露。**

🔴 **Model 向外广播的重要事件必须通过 EventBus，由跨系统模块订阅。**

🟡 **如果某事件既要更新本模块 UI，又要通知其他模块，那么：**
- 本模块 Presenter 与 Model 建立即时回调（内部）
- 同时 Model 通过 EventBus 广播（外部）

