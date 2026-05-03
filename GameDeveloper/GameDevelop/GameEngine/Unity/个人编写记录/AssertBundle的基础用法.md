## 创建AssertBundle

### 方法一：使用脚本创建
```csharp
using System.IO;
using UnityEditor;

public class CreateAssetBundles 
{
    [MenuItem("Assets/BuildAssetBundles")]
    static void BuildAllAssetBundles()
    {
        string path = "AssetBundles";
        if (Directory.Exists(path) == false)//判断是否存在path目录
        {
            Directory.CreateDirectory(path);
        }
        BuildPipeline.BuildAssetBundles(path, BuildAssetBundleOptions.None, BuildTarget.StandaloneWindows64);
    }
}

```


### 方法二：使用AssertBundle Browser插件
#### Installation

To install the Asset Bundle Browser:

* Open the Unity Package Manager in your Project (menu: Windows > Package Manager).

* Click the + (Add) button at the top, left corner of the window.

* Choose Add package from git URL…

* Enter https://github.com/Unity-Technologies/AssetBundles-Browser.git as the URL

* Click Add.

The Package Manager downloads and installs the package’s “master” branch.

Once installed it will create a new menu item in *Window->AssetBundle Browser*.

## 通过AssertBundle创建实例
```csharp
using UnityEngine;  
  
public class AssertLoader: MonoBehaviour  
{  
    // Start is called before the first frame update  
    void Start()  
    {        AssetBundle ab = AssetBundle.LoadFromFile("AssetBundles/StandaloneWindows/bed.unity3d");//这里是路径名  
        GameObject wall = ab.LoadAsset<GameObject>("Bed");//这里的名字是加载的资源模型名字  
        Instantiate(wall, Vector3.zero, Quaternion.identity);  
    }}

```