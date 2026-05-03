在Unity中，以下几种类型是可以序列化到编辑器中以供编辑的：

1. **基本数据类型**：
   - `int`, `float`, `double`, `bool`, `char`, `string`, `enum`
   
2. **Unity自带的类型**：
   - `Vector2`, `Vector3`, `Vector4`, `Quaternion`, `Color`, `Rect`, `Bounds`, `Matrix4x4`, `AnimationCurve`, `LayerMask`
   - `GameObject`, `Transform`, `MonoBehaviour`, `ScriptableObject`, `Component`
   
3. **数组和列表**：
   - 数组（如 `int[]`, `float[]`, `string[]` 等）
   - `List<T>` 类型，前提是 `T` 是可以序列化的类型（如 `List<int>`, `List<string>` 等）
   
4. **自定义类和结构体**：
   - 如果自定义的类或结构体上标记了 `[System.Serializable]` 特性，它们就可以在编辑器中序列化。例如：
     ```csharp
     [System.Serializable]
     public class MyClass
     {
         public int myInt;
         public string myString;
     }
     ```

5. **Unity自带的集合类型**：
   - `Dictionary<TKey, TValue>` 和 `HashSet<T>` 不能直接序列化。但可以通过自定义的序列化方式或者使用 `SerializableDictionary` 插件等方法进行序列化。
   
6. **枚举类型**：
   - 任何定义了的 `enum` 类型都可以序列化。
   
7. **Unity中的`ScriptableObject`**：
   - 通过继承 `ScriptableObject` 的类可以在编辑器中保存数据并进行编辑。

在Unity编辑器中，如果需要某个字段能够序列化显示并被编辑，通常需要将该字段设置为公共字段(`public`)或者使用 `[SerializeField]` 特性标记私有字段。这些字段将在Unity的Inspector面板中显示并可以进行修改。

### 注意：
- 对于非基本数据类型（例如自定义的类或结构体），必须加上 `[System.Serializable]` 特性才会被序列化。
- 私有字段可以通过 `[SerializeField]` 标记，使它们在编辑器中可见并可编辑。

如果有其他类型或细节问题，欢迎继续询问！