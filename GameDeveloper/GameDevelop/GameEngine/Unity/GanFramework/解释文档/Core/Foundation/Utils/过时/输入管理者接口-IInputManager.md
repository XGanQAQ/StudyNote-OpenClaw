```cs
using UnityEngine;  
  
namespace Core  
{  
    public interface IInputManager  
    {  
        public Vector2 Move { get; }  
        public Vector2 Look { get; }  
        public void SetCursorState(bool visible, CursorLockMode lockMode);  
        public void SetInputForLook(bool enabled);  
        public void SetInputForMove(bool enabled);  
    }}
```

因为输入管理器的按键和Gameplay的耦合很大，所以具体IInputManager的实现在Gameplay中去实现。