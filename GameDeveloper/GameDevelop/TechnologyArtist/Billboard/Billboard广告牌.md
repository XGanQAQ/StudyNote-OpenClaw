# Billboard 广告牌

## 什么是 Billboard

Billboard 是一种图形技术，用于使二维平面对象（如纹理）始终面向摄像机，从而在三维场景中实现“始终朝向玩家”或“始终正面显示”的效果。这种效果在游戏开发和可视化中广泛应用于显示树木、云朵、UI元素、敌人血条等，使其看起来总是正对着摄像机，即便摄像机移动或旋转。

## Billboard 使用场景

Billboard 技术在以下场景中经常被应用：
- **自然环境**：例如树木、草地、云朵等需要节省性能的场景，Billboard 可以代替真实的 3D 模型，用二维纹理模拟这些物体。
- **UI 元素**：游戏中的血条、标签等 HUD 元素可以使用 Billboard，使这些元素始终面向玩家视角。
- **特效**：如爆炸、火焰、烟雾等特效，利用 Billboard 使平面特效始终面向玩家，提供更好的视觉效果。
- **虚拟角色头像**：用于在场景中指示角色方向的头像图标或目标图标。

## Billboard 的实现原理

Billboard 的实现原理包括以下几个步骤：

### 实时获得摄像机位置

为了让对象始终朝向摄像机，我们需要在每帧实时获取摄像机的位置。大多数渲染管线会提供一个全局的 `_WorldSpaceCameraPos` 变量，表示摄像机在世界坐标中的位置。在 Unity 的 Shader 中，可以通过该变量获得摄像机的位置，用于计算物体相对于摄像机的方向。

### 计算物体的新坐标系

根据摄像机和对象的位置，可以构建一个新的坐标系，以使对象面向摄像机。具体步骤如下：

1. **计算朝向向量**：计算从对象指向摄像机的方向向量 `CameraVector`。
2. **构建基向量**：
   - 使用一个虚拟的上方向向量 `tempUp`（通常为 `(0, 1, 0)`）和 `CameraVector` 进行叉乘，得到对象的**右向量** `rightVector`，这是新的坐标系的第一条基向量。
   - 然后，用 `rightVector` 和 `CameraVector` 进行叉乘，得到新的坐标系的**上向量** `upVector`。
3. **构造新的垂直坐标系**：`CameraVector`、`rightVector` 和 `upVector` 构成了一个新的正交坐标系，该坐标系可以让对象始终面向摄像机。

### 使用新坐标系计算新位置

在传统的局部坐标系下，物体的 `x`、`y`、`z` 分量代表其位置。为了实现 Billboard 效果，我们只需要将这些分量分别乘以新的 `rightVector`、`upVector` 和 `CameraVector`，从而在新的坐标系中计算出物体的最终位置。

具体来说，物体的原始坐标可以表示为：
$$
\text{newPos} = \text{rightVector} \cdot \text{ObjectPos.x} + \text{upVector} \cdot \text{ObjectPos.y} + \text{CameraVector} \cdot \text{ObjectPos.z}
$$

## Unity URP 实现 Billboard

在 Unity 的 URP 中，我们可以通过 Shader 来实现 Billboard 效果。

### 基本实现

以下代码展示了基本的 Billboard 实现：

```csharp
float3 RecalculateAsBillboard(float3 ObjectPos)
{
    // 将摄像机的世界坐标转换到对象坐标系中
    float3 CameraPos = mul(unity_WorldToObject, float4(_WorldSpaceCameraPos, 1.0)).xyz;
    
    // 计算对象坐标系下的摄像机方向
    float3 CameraVector = normalize(CameraPos - ObjectPos);

    // 定义上方向
    float3 tempUp = float3(0.0, 1.0, 0.0);

    // 计算右方向和上方向
    float3 rightVector = normalize(cross(tempUp, CameraVector));
    float3 upVector = normalize(cross(rightVector, CameraVector));

    // 使用对象坐标重新构建 Billboard 的位置
    float3 newPos = rightVector * ObjectPos.x + upVector * ObjectPos.y + CameraVector * ObjectPos.z;

    return newPos;
}
```

float4版本
```cs
float4 RecalculateAsBillboard(float4 ObjectPos)
{
    // 将摄像机的世界坐标转换到对象坐标系中
    float3 CameraPos = mul(unity_WorldToObject, float4(_WorldSpaceCameraPos, 1.0)).xyz;

    // 对象坐标
    float3 objPos = ObjectPos.xyz;

    // 计算对象坐标系下的摄像机方向
    float3 CameraVector = normalize(CameraPos - objPos);

    // 定义上方向（对象空间）
    float3 tempUp = float3(0.0, 1.0, 0.0);

    // 计算右方向和上方向
    float3 rightVector = normalize(cross(tempUp, CameraVector));
    float3 upVector    = normalize(cross(rightVector, CameraVector));

    // 使用对象坐标重新构建 Billboard 的位置
    float3 newPos =
        rightVector * objPos.x +
        upVector    * objPos.y +
        CameraVector * objPos.z;

    // 返回 float4，w 保持不变
    return float4(newPos, ObjectPos.w);
}
```
### 优化问题

#### 让 Billboard 只会水平旋转，不会上下旋转

为了限制 Billboard 仅在水平平面上旋转，而不随摄像机的上下视角变化，可以将 `CameraVector` 的 `y` 分量设为零。这会忽略垂直方向的影响，使 Billboard 仅在水平面内旋转：

```csharp
CameraVector.y = CameraVector.y * _VerticalBillboard;
```

这里 `_VerticalBillboard` 是一个控制开关，通常为 `0`（不考虑垂直旋转）或 `1`（允许垂直旋转）。

#### 当相机位于正上方时的向量重合问题

当摄像机位于对象正上方时，向量 `CameraVector` 和 `tempUp` 可能会接近重合，导致无法正确计算 `rightVector`。为了解决这个问题，可以动态调整 `tempUp` 方向。例如，当 `CameraVector.y` 非常接近 `1.0` 时，将 `tempUp` 设置为 Z 轴方向：

```csharp
float3 tempUp = abs(CameraVector.y) > 0.999 ? float3(0, 0, 1) : float3(0, 1, 0);
```

#### 可能出现 UV 颠倒的情况

由于不同的摄像机角度或向量方向计算，可能会导致 Billboard 的 UV 贴图出现翻转现象。为了解决这个问题，可以使用 `dot` 产品来判断向量方向，并根据需要对 UV 进行调整，以保持贴图始终在正确方向。

#### 坐标的矩阵乘法变化与坐标的乘法累加变化区别

- **矩阵乘法**：坐标变换使用矩阵乘法不会改变实际顶点的位置，而是更改坐标系。例如，通过矩阵变换，物体会在新坐标系中显示不同的位置和朝向，但不会影响原始位置。
  
- **乘法累加**：累加操作直接更改顶点的实际位置，将原始坐标分量分别与新的基向量相乘累加，从而更改顶点在新坐标系中的位置。这种方法更适合动态调整每个顶点，使其在新的坐标系中位置随时更新。

通过这些步骤，你可以在 Unity URP 中实现一个灵活的 Billboard 效果。

## 参考
[bilbil小坛子熊的视频](https://www.bilibili.com/video/BV18NSoY6EnB)