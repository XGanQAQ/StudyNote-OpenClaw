## 参考来源
[Unity-ARPGGameDemo-TheDawnAbyss/Scripts/GameBase/MonoSingleton.cs at main · HalfADog/Unity-ARPGGameDemo-TheDawnAbyss](https://github.com/HalfADog/Unity-ARPGGameDemo-TheDawnAbyss/blob/main/Scripts/GameBase/MonoSingleton.cs)

##
```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MonoSingleton<T> : MonoBehaviour where T : MonoBehaviour
{
	private static T instance;
	public static T Instance 
	{
		get
		{
			if (instance == null)
			{
				instance = FindObjectOfType<T>();
				if (instance == null)
				{
					GameObject gameObject = new GameObject();
					instance = gameObject.AddComponent<T>();
				}
			}
			return instance;
		}
	}

	protected virtual void Awake()
	{
		if (instance == null)
		{
			instance = this as T;
			return;
		}
		if (instance != this as T)
		{
			Destroy(gameObject);
		}
	}
}
```

`where T : MonoBehaviour` 的实际意义在于：
1. **类型安全**：确保传入的类型能合法地被当作 Unity 脚本使用。
2. **编译器支持**：允许使用 `AddComponent<T>()` 等 MonoBehaviour 专属功能。
3. **语义正确**：MonoSingleton 设计就是为了创建“有场景存在的单例对象”，而不是纯逻辑类。