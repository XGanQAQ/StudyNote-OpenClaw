```cs
using UnityEngine;  
using UnityEngine.SceneManagement;  
using System.Collections;  
  
namespace Core  
{  
    public class ScenesManager : MonoBehaviour  
    {  
        public static ScenesManager Instance { get; private set; }  
  
        private string currentGameplayScene;  
  
        private bool IsLoadGameplayUI = false;  
  
        void Awake()  
        {            if (Instance != null)  
            {                Destroy(gameObject);  
                return;  
            }            Instance = this;  
            //DontDestroyOnLoad(gameObject);  
        }  
  
        public void LoadMainMenu()  
        {            if (IsLoadGameplayUI)  
            {                // 如果已经加载过游戏内UI场景，则卸载掉  
                StartCoroutine(UnloadScene("UIScene"));  
                IsLoadGameplayUI = false;  
            }            // 加载主菜单场景，需要卸载掉除了Core以外的所有场景  
            StartCoroutine(SwitchGameplay("StartMenu"));  
        }  
  
        public void LoadGameplay(string sceneName)  
        {            StartCoroutine(SwitchGameplay(sceneName));  
            if (!IsLoadGameplayUI)  
            {                // 只加载一次游戏内UI场景  
                StartCoroutine(LoadSceneAdditive("UIScene"));  
                IsLoadGameplayUI = true;  
            }        }  
        /// <summary>  
        /// 切换游戏场景，卸载当前的游戏场景，加载新的游戏场景  
        /// 适用于在游戏内切换场景  
        /// </summary>  
        /// <param name="newScene"></param>        /// <returns></returns>        private IEnumerator SwitchGameplay(string newScene)  
        {            if (!string.IsNullOrEmpty(currentGameplayScene))  
            {                yield return UnloadScene(currentGameplayScene);  
            }            yield return LoadSceneAdditive(newScene);  
            currentGameplayScene = newScene;  
        }  
        private IEnumerator LoadSceneAdditive(string sceneName)  
        {            var async = UnityEngine.SceneManagement.SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Additive);  
            while (!async.isDone)  
            {                yield return null;  
            }        }  
        private IEnumerator UnloadScene(string sceneName)  
        {            var async = UnityEngine.SceneManagement.SceneManager.UnloadSceneAsync(sceneName);  
            while (!async.isDone)  
            {                yield return null;  
            }        }    }}
```