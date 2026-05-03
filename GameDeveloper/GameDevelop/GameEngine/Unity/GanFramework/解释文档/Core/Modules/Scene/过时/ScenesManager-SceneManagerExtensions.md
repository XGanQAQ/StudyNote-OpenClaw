```cs
using System.Collections.Generic;  
using Core;  
using UnityEngine;  
using Utils.Extensions;  
  
namespace Gameplay.Global  
{  
    using UnityEngine;  
    using UnityEngine.SceneManagement;    using System.Collections;  
  
    public class ScenesManager : PersistentSingleton<ScenesManager>  
    {        public void LoadMainMenu()  
        {            // 加载主菜单场景，需要卸载掉除了Core以外的所有场景  
            List<string> loadedScenes = SceneManagerExtensions.GetLoadedSceneNames();  
            foreach (var scene in loadedScenes)  
            {                if (scene != "Core" && scene != "MainMenu")  
                {                    StartCoroutine(SceneManagerExtensions.UnloadSceneCoroutine(scene));  
                }            }            StartCoroutine(SceneManagerExtensions.LoadSceneAdditiveCoroutine("MainMenu"));  
        }  
  
        public void LoadGameplay(string sceneName)  
        {            StartCoroutine(SwitchGameplay(sceneName));  
        }  
        /// <summary>  
        /// 切换游戏场景，卸载当前的游戏场景，加载新的游戏场景  
        /// 适用于在游戏内切换场景  
        /// </summary>  
        /// <param name="newScene"></param>        /// <returns></returns>        private IEnumerator SwitchGameplay(string newScene)  
        {            // 卸载掉除了 Core 和 UIScene 以外的所有场景  
            List<string> loadedScenes = SceneManagerExtensions.GetLoadedSceneNames();  
            foreach (var scene in loadedScenes)  
            {                if (scene != "Core" && scene != "UIScene")  
                {                    yield return SceneManagerExtensions.UnloadSceneCoroutine(scene);  
                }            }            // 加载UI场景（如果还没加载的话）  
            if (!SceneManagerExtensions.IsLoadedScene("UIScene"))  
            {                // 只加载一次游戏内UI场景  
                StartCoroutine(SceneManagerExtensions.LoadSceneAdditiveCoroutine("UIScene"));  
            }  
            // 加载新的游戏场景  
            yield return SceneManagerExtensions.LoadSceneAdditiveCoroutine(newScene);  
        }    }}
```

```cs
using System.Collections;  
using System.Collections.Generic;  
using UnityEngine;  
using UnityEngine.SceneManagement;  
  
namespace Utils.Extensions  
{  
    public static class SceneManagerExtensions  
    {  
        public static bool IsLoadedScene(string sceneName)  
        {            for (int i = 0; i < SceneManager.sceneCount; i++)  
            {                var scene = SceneManager.GetSceneAt(i);  
                if (scene.isLoaded && scene.name == sceneName)  
                    return true;  
            }  
            return false;  
        }  
        // 返回当前所有已加载场景的名称列表  
        public static List<string> GetLoadedSceneNames()  
        {            var names = new List<string>();  
            for (int i = 0; i < SceneManager.sceneCount; i++)  
            {                var scene = SceneManager.GetSceneAt(i);  
                if (scene.isLoaded)  
                    names.Add(scene.name);  
            }  
            return names;  
        }  
        // 打印已加载场景到控制台  
        public static void LogLoadedScenes()  
        {            var names = GetLoadedSceneNames();  
            Debug.Log("Loaded Scenes: " + string.Join(", ", names));  
        }  
        // 可用于 StartCoroutine 的异步加载（Additive）  
        public static IEnumerator LoadSceneAdditiveCoroutine(string sceneName)  
        {            var async = SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Additive);  
            if (async == null)  
            {                Debug.LogWarning($"LoadSceneAsync returned null for scene '{sceneName}'");  
                yield break;  
            }  
            while (!async.isDone) yield return null;  
        }  
        // 可用于 StartCoroutine 的异步卸载  
        public static IEnumerator UnloadSceneCoroutine(string sceneName)  
        {            var async = SceneManager.UnloadSceneAsync(sceneName);  
            if (async == null)  
            {                Debug.LogWarning($"UnloadSceneAsync returned null for scene '{sceneName}'");  
                yield break;  
            }  
            while (!async.isDone) yield return null;  
        }    }}
```