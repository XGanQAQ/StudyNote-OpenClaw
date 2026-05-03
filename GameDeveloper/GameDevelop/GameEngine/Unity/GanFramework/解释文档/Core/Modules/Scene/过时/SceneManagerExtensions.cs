using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Utils.Extensions
{
    public static class SceneManagerExtensions
    {
        public static bool IsLoadedScene(string sceneName)
        {
            for (int i = 0; i < SceneManager.sceneCount; i++)
            {
                var scene = SceneManager.GetSceneAt(i);
                if (scene.isLoaded && scene.name == sceneName)
                    return true;
            }

            return false;
        }

        // 返回当前所有已加载场景的名称列表
        public static List<string> GetLoadedSceneNames()
        {
            var names = new List<string>();
            for (int i = 0; i < SceneManager.sceneCount; i++)
            {
                var scene = SceneManager.GetSceneAt(i);
                if (scene.isLoaded)
                    names.Add(scene.name);
            }

            return names;
        }

        // 打印已加载场景到控制台
        public static void LogLoadedScenes()
        {
            var names = GetLoadedSceneNames();
            Debug.Log("Loaded Scenes: " + string.Join(", ", names));
        }

        // 可用于 StartCoroutine 的异步加载（Additive）
        public static IEnumerator LoadSceneAdditiveCoroutine(string sceneName)
        {
            var async = SceneManager.LoadSceneAsync(sceneName, LoadSceneMode.Additive);
            if (async == null)
            {
                Debug.LogWarning($"LoadSceneAsync returned null for scene '{sceneName}'");
                yield break;
            }

            while (!async.isDone) yield return null;
        }

        // 可用于 StartCoroutine 的异步卸载
        public static IEnumerator UnloadSceneCoroutine(string sceneName)
        {
            var async = SceneManager.UnloadSceneAsync(sceneName);
            if (async == null)
            {
                Debug.LogWarning($"UnloadSceneAsync returned null for scene '{sceneName}'");
                yield break;
            }

            while (!async.isDone) yield return null;
        }
    }
}