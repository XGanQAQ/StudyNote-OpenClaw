使用 **Scriptable Object** 是 Unity 中管理和共享数据的有效方法。通过 Scriptable Object，你可以创建自定义的数据类型，并将其存储为项目中的资产，方便多个对象或场景共享和修改。

### **使用 Scriptable Object 的步骤**

#### **1. 创建 Scriptable Object 类**
首先，你需要创建一个继承自 `ScriptableObject` 的自定义类来定义你的数据结构。这个类不需要附加到任何 GameObject 上，它只是数据容器。

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewItem", menuName = "Game/Item")]
public class Item : ScriptableObject
{
    public string itemName;
    public int itemID;
    public float itemValue;
}
```

- `[CreateAssetMenu]` 特性使得你能够在 Unity 编辑器中通过右键菜单创建该 Scriptable Object 实例。
- `fileName` 指定了创建文件时的默认名称，`menuName` 定义了右键菜单中的分类。

#### **2. 在编辑器中创建 Scriptable Object 实例**
1. 右键点击项目视图中的 `Assets` 文件夹，选择 **Create > Scriptable Object > Item**。
2. 创建后，你会得到一个 `.asset` 文件，这个文件保存了你的 `Item` 实例。

#### **3. 在脚本中引用 Scriptable Object**
你可以将 Scriptable Object 引用到 `MonoBehaviour` 脚本中，通过编辑器将资产拖入到脚本的字段中，或者通过代码动态加载它们。

**在脚本中引用 Scriptable Object**：
```csharp
using UnityEngine;

public class Inventory : MonoBehaviour
{
    public Item item; // 在编辑器中拖拽Item实例到这里

    void Start()
    {
        Debug.Log($"Item: {item.itemName}, Value: {item.itemValue}");
    }
}
```

1. 将 `Inventory` 脚本挂载到一个 GameObject 上。
2. 在 `Inspector` 窗口中，你会看到 `Item` 字段，可以将你创建的 Scriptable Object 实例拖动到该字段中。

#### **4. 动态创建 Scriptable Object 实例（运行时）**
你也可以通过代码动态创建 Scriptable Object 实例，这种方式不依赖于编辑器中的资产文件。

```csharp
void Start()
{
    Item newItem = ScriptableObject.CreateInstance<Item>();
    newItem.itemName = "Sword";
    newItem.itemValue = 100f;
    
    Debug.Log($"Item: {newItem.itemName}, Value: {newItem.itemValue}");
}
```

这样创建的实例是运行时临时的，不会保存到项目文件中。

#### **5. 修改和保存 Scriptable Object**
如果你修改了通过编辑器引用的 Scriptable Object 数据，Unity 会自动更新该资产文件的内容。为了确保在编辑器中保存更改，可以使用 `AssetDatabase.SaveAssets()`：

```csharp
#if UNITY_EDITOR
using UnityEditor;

void SaveItem(Item item)
{
    EditorUtility.SetDirty(item);
    AssetDatabase.SaveAssets();
}
#endif
```

---

### **优点总结**
- **数据共享**：多个场景和对象可以共享同一个 Scriptable Object 实例。
- **内存效率**：不同的脚本可以引用相同的 Scriptable Object，而不需要多次存储相同的数据。
- **易于维护**：数据与逻辑分离，使得管理和修改变得更直观。

Scriptable Object 非常适合用来管理配置数据、游戏状态、关卡设置等静态或全局的数据，并可以有效地在项目中进行复用。

## 注意
- 在编辑器界面中启动游戏状态下，对ScriptObject的数据进行修改会被保存
- **打包后**的游戏（Player / Build）里，对 ScriptableObject 的修改绝对**不会被“保存**回资源文件”。
