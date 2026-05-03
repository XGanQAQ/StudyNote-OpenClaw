---
tags:
  - "#CSharp"
---

Lazy法
```csharp
using System;

public class AudioManager
{
    private static readonly Lazy<AudioManager> _instance = 
        new Lazy<AudioManager>(() => new AudioManager());

    public static AudioManager Instance => _instance.Value;

    private AudioManager() 
    {
        // 初始化逻辑
    }

    public void PlaySound(string soundName)
    {
        Debug.Log($"Playing sound: {soundName}");
    }
}
```

Unity的MonoBehaviour法