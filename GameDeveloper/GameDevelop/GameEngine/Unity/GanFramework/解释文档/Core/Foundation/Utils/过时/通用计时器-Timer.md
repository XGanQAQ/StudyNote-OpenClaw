```cs
using System;  
  
namespace Core  
{  
    public class Timer  
    {  
        public float Duration { get; private set; }  
        public float Elapsed { get; private set; }  
        public bool IsRunning { get; private set; }  
        public bool IsFinished { get; private set; }  
        public bool Loop { get; set; }  
        public Action OnFinished { get; set; }  
  
        public float Remaining => Math.Max(0f, Duration - Elapsed);  
        public float Progress => Duration <= 0f ? 1f : Math.Clamp(Elapsed / Duration, 0f, 1f);  
  
        public Timer(float duration, bool autoStart = false, bool loop = false, Action onFinished = null)  
        {            Duration = Math.Max(0f, duration);  
            Loop = loop;  
            OnFinished = onFinished;  
            Reset();  
            if (autoStart) Start();  
        }  
        public void Start()  
        {            if (IsFinished && !Loop) return;  
            IsRunning = true;  
        }  
        public void Pause()  
        {            IsRunning = false;  
        }  
        public void Stop()  
        {            IsRunning = false;  
            IsFinished = true;  
        }  
        public void Reset(float? duration = null)  
        {            if (duration.HasValue) Duration = Math.Max(0f, duration.Value);  
            Elapsed = 0f;  
            IsFinished = Duration <= 0f;  
            IsRunning = false;  
        }  
        // 返回值：本次 Update 是否触发了完成事件  
        public bool Update(float deltaTime)  
        {            if (!IsRunning || IsFinished) return false;  
            if (deltaTime <= 0f) return false;  
  
            Elapsed += deltaTime;  
  
            if (Elapsed >= Duration)  
            {                OnFinished?.Invoke();  
  
                if (Loop && Duration > 0f)  
                {                    // 支持多圈跨帧累加  
                    Elapsed = Elapsed % Duration;  
                    IsFinished = false;  
                    return true;  
                }                else  
                {  
                    Elapsed = Duration;  
                    IsFinished = true;  
                    IsRunning = false;  
                    return true;  
                }            }  
            return false;  
        }    }}
```