

> **选中一个或多个 GameObject → 一键把它们所有子物体上的 TextMeshPro 字体替换成你指定的字体**

---

## 功能说明

- 支持 **TextMeshProUGUI** 和 **TextMeshPro（3D）**
    
- 会递归查找 **选中对象及其所有子对象**
    
- 支持 **多选**
    
- 使用 Unity Editor 窗口操作（安全、直观）
    
- 支持 Undo（可撤销）
    

---

## 使用方式

1. 在工程中创建目录（如果没有）
    
    ```
    Assets/Editor/
    ```
    
2. 新建脚本
    
    ```
    TMPFontBatchSwitcher.cs
    ```
    
3. 把下面代码 **完整复制进去**
    

---

## 编辑器脚本代码

```csharp
using UnityEngine;
using UnityEditor;
using TMPro;

public class TMPFontBatchSwitcher : EditorWindow
{
    private TMP_FontAsset targetFont;

    [MenuItem("Tools/TextMeshPro/Batch Switch Font")]
    public static void ShowWindow()
    {
        GetWindow<TMPFontBatchSwitcher>("TMP Font Switcher");
    }

    private void OnGUI()
    {
        GUILayout.Label("批量替换 TextMeshPro 字体", EditorStyles.boldLabel);

        targetFont = (TMP_FontAsset)EditorGUILayout.ObjectField(
            "目标字体",
            targetFont,
            typeof(TMP_FontAsset),
            false
        );

        EditorGUILayout.Space();

        using (new EditorGUI.DisabledScope(targetFont == null))
        {
            if (GUILayout.Button("替换选中对象及其子物体中的 TMP 字体"))
            {
                ReplaceFont();
            }
        }

        EditorGUILayout.HelpBox(
            "会递归替换选中 GameObject 下所有 TextMeshPro / TextMeshProUGUI 的字体",
            MessageType.Info
        );
    }

    private void ReplaceFont()
    {
        GameObject[] selectedObjects = Selection.gameObjects;
        if (selectedObjects.Length == 0)
        {
            EditorUtility.DisplayDialog("提示", "请先选择一个或多个 GameObject", "OK");
            return;
        }

        int count = 0;

        foreach (var root in selectedObjects)
        {
            // TextMeshProUGUI
            var uguiTexts = root.GetComponentsInChildren<TextMeshProUGUI>(true);
            foreach (var tmp in uguiTexts)
            {
                Undo.RecordObject(tmp, "Change TMP Font");
                tmp.font = targetFont;
                EditorUtility.SetDirty(tmp);
                count++;
            }

            // TextMeshPro (3D)
            var worldTexts = root.GetComponentsInChildren<TextMeshPro>(true);
            foreach (var tmp in worldTexts)
            {
                Undo.RecordObject(tmp, "Change TMP Font");
                tmp.font = targetFont;
                EditorUtility.SetDirty(tmp);
                count++;
            }
        }

        Debug.Log($"TMP 字体替换完成，共修改 {count} 个 TextMeshPro 组件");
    }
}
```

---

## 使用步骤（实际操作）

1. 在 **Hierarchy** 中选中一个或多个对象（UI 根节点、Canvas、Prefab 实例都行）
    
2. 打开菜单：
    
    ```
    Tools → TextMeshPro → Batch Switch Font
    ```
    
3. 拖入你想使用的 `TMP_FontAsset`
    
4. 点击 **“替换选中对象及其子物体中的 TMP 字体”**
    
5. 完成 ✅（支持 Ctrl+Z 撤销）
    

---

## 常见扩展（如果你之后需要）

你之后可以很容易加这些功能：

- ✅ 只替换 **UGUI / 3D** 其中一种
    
- ✅ 过滤某些名字（如 `Ignore`、`DebugText`）
    
- ✅ 同时批量修改：
    
    - Font Size
        
    - Line Spacing
        
    - Alignment
        
- ✅ 对 **Prefab 资产本身** 批量生效（用 `PrefabUtility`）