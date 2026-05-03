游戏具体输入有哪些按键是和Gameplay强关联的，所以作为Gameplay参考代码的一部分

关于按键的绑定，最后不要在非InputManager的地方，直接通过自助生成的输入类来绑定按键，因为你可能会因为没能在对象消失的时候，注销掉按键绑定的事件，导致内存泄露。

```cs
using UnityEngine;  
using UnityEngine.InputSystem;  
  
namespace Core  
{  
    public class InputManager : MonoSingleton<InputManager>  
    {        private PlayerInputActions _input; // 自动生成的输入类  
  
        // 当前输入值  
        public Vector2 Move { get; private set; }  
        public Vector2 Look { get; private set; }  
        public bool JumpPressed { get; private set; }  
        public bool AttackPressed { get; private set; }  
        public bool PausePressed { get; private set; }  
  
        private void Awake()  
        {            _input = new PlayerInputActions();  
        }  
        private void OnEnable()  
        {            _input.Enable();  
  
            // 注册事件  
            _input.Player.Move.performed += ctx => Move = ctx.ReadValue<Vector2>();  
            _input.Player.Move.canceled += ctx => Move = Vector2.zero;  
  
            _input.Player.Look.performed += ctx => Look = ctx.ReadValue<Vector2>();  
            _input.Player.Look.canceled += ctx => Look = Vector2.zero;  
            //  
            // _input.Player.Jump.performed += ctx => JumpPressed = true;            // _input.Player.Jump.canceled += ctx => JumpPressed = false;            //  
        }  
  
        private void OnDisable()  
        {            _input.Disable();  
        }  
        private void Update()  
        {            // 在此更新一次性触发的输入，例如“按下瞬间触发”  
            if (PausePressed)  
            {                Debug.Log("Pause Pressed!");  
                PausePressed = false; // 手动清除  
            }  
        }  
        // 🔧 示例方法：允许外部模块手动启用/禁用输入（比如暂停菜单）  
        public void SetInputEnabled(bool enabled)  
        {            if (enabled) _input.Enable();  
            else _input.Disable();  
        }  
        public void SetCursorState(bool visible, CursorLockMode lockMode)  
        {            Cursor.visible = visible;  
            Cursor.lockState = lockMode;  
        }  
        public void SetInputForLook(bool enabled)  
        {            if (enabled)  
            {                _input.Player.Look.Enable();  
            }            else  
            {  
                _input.Player.Look.Disable();  
                Look = Vector2.zero; // 禁用时清除Look值  
            }  
        }  
        public void SetInputForMove(bool enabled)  
        {            if (enabled)  
            {                _input.Player.Move.Enable();  
            }            else  
            {  
                _input.Player.Move.Disable();  
                Move = Vector2.zero; // 禁用时清除Move值  
            }  
        }    }}
```

