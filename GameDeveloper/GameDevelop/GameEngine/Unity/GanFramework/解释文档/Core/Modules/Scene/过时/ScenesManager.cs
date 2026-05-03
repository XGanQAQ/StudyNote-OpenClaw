using System.Collections.Generic;
using Core;
using UnityEngine;
using Utils.Extensions;

namespace Gameplay.Global
{
    using UnityEngine;
    using UnityEngine.SceneManagement;
    using System.Collections;

    public class ScenesManager : PersistentSingleton<ScenesManager>
    {
        public void LoadMainMenu()
        {
            // 加载主菜单场景，需要卸载掉除了Core以外的所有场景
            List<string> loadedScenes = SceneManagerExtensions.GetLoadedSceneNames();
            foreach (var scene in loadedScenes)
            {
                if (scene != "Core" && scene != "MainMenu")
                {
                    StartCoroutine(SceneManagerExtensions.UnloadSceneCoroutine(scene));
                }
            }
            
            StartCoroutine(SceneManagerExtensions.LoadSceneAdditiveCoroutine("MainMenu"));
        }


        public void LoadGameplay(string sceneName)
        {
            StartCoroutine(SwitchGameplay(sceneName));
        }

        /// <summary>
        /// 切换游戏场景，卸载当前的游戏场景，加载新的游戏场景
        /// 适用于在游戏内切换场景
        /// </summary>
        /// <param name="newScene"></param>
        /// <returns></returns>
        private IEnumerator SwitchGameplay(string newScene)
        {
            // 卸载掉除了 Core 和 UIScene 以外的所有场景
            List<string> loadedScenes = SceneManagerExtensions.GetLoadedSceneNames();
            foreach (var scene in loadedScenes)
            {
                if (scene != "Core" && scene != "UIScene")
                {
                    yield return SceneManagerExtensions.UnloadSceneCoroutine(scene);
                }
            }
            
            // 加载UI场景（如果还没加载的话）
            if (!SceneManagerExtensions.IsLoadedScene("UIScene"))
            {
                // 只加载一次游戏内UI场景
                StartCoroutine(SceneManagerExtensions.LoadSceneAdditiveCoroutine("UIScene"));
            }

            // 加载新的游戏场景
            yield return SceneManagerExtensions.LoadSceneAdditiveCoroutine(newScene);
        }
    }
}