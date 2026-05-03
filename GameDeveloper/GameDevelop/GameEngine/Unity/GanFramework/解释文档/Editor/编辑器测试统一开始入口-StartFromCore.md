```cs
// 文件路径：Assets/Editor/StartFromCore.cs  
using UnityEditor;  
using UnityEditor.SceneManagement;  
using UnityEngine;  
  
namespace Editor  
{  
    public static class StartFromCore  
    {  
        // 菜单路径：Tools/Start From Core   快捷键：Ctrl+Shift+C  
        [MenuItem("Tools/Start From Core %#c", false, 0)]  
        private static void StartFromCoreScene()  
        {            if (EditorApplication.isPlaying)  
            {                Debug.Log("已在 Play 模式，忽略重复操作。");  
                return;  
            }  
            string coreScenePath = "Assets/Scenes/Core.unity";  
            var coreScene = AssetDatabase.LoadAssetAtPath<SceneAsset>(coreScenePath);  
  
            if (coreScene == null)  
            {                EditorUtility.DisplayDialog(  
                    "找不到 Core 场景",  
                    $"请在 {coreScenePath} 放置名为 Core 的场景文件。",  
                    "确定");  
                return;  
            }  
            // 保存当前场景（可选）  
            if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())  
            {                // 把 Core 场景设置成“唯一”启动场景  
                EditorSceneManager.playModeStartScene = AssetDatabase.LoadAssetAtPath<SceneAsset>(coreScenePath);  
  
                // 进入 Play 模式  
                EditorApplication.EnterPlaymode();  
            }        }  
        // 当正在播放时禁用菜单  
        [MenuItem("Tools/Start From Core", true)]  
        private static bool ValidateStartFromCoreScene() => !EditorApplication.isPlaying;  
    }}
```