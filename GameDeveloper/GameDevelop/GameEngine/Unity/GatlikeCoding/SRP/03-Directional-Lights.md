## 1. Lighting

### 1.1 Lit Shader

我们复制上一章的Unlit shader 编写 Lit shader

### 1.2 Normal Vectors

添加法线属性

### 1.3 Interpolated Normals

在顶点围成的三角形之内，会对法线进行线性差值 linear interpolation 这会影响这些差值法线的长度，不会是准确的单位长度，存在误差
```cs
// 可视化放大法线长度误差
base.rgb = abs(length(input.normalWS) - 1.0) * 10.0;
```

### 1.4 Surface Properties

光照Shader是关于模拟光和物体表面交互的Shader。

为了方便追踪表面属性，我们定义一个 Surface 结构体
- Surface
	- float3 normal 法线
	- float3 color 表面rgb颜色
	- float alpha 透明度

>The struct is purely for our convenience.

>[!question] 为什么光照计算可以在任何3D空间下？
>光照计算的核心是确定光线、表面法线和视线方向之间的关系。这些关系是几何性质，它们在不同空间中虽然表示的坐标值不同，但**相对关系**是不变的。只要我们知道光照计算所需的必要信息（位置、法线、光线方向、视线方向等）在哪个空间中，并确保这些信息处于**同一个空间中**，我们就可以进行计算。

### 1.5 Calculating Lighting

我们新建一个hlsl文件，专门存放计算光照的函数`GetLighting` 我们先简单计算一下

## 2. Light

### 2.1 Light Structure

>the light's direction is thus defined as the direction from where the light is coming, not where it is going.

### 2.2 Lighting Functions

>[!question] saturate 的作用是什么？
>Returns _x_ saturated to the range [0,1] as follows:
>1) Returns 0 if _x_ is less than 0; else
>2) Returns 1 if _x_ is greater than 1; else
>3) Returns _x_ otherwise.
For vectors, the returned vector contains the saturated result of each element of the vector _x_ saturated to [0,1].

我们定义了计算给定表面和光源的入射光量的函数 `IncomingLight`

### 2.3 Sending Light Data to the GPU

我们将给光源位置分配缓冲区，让其发送到GPU中，我们在通过GPU去读取。

我们创建了一个Lghting的C#类，用来设置光照信息。（他的工作原理和CameraRenderer类似，这种原理是什么？）

### 2.4 Visible Lights 可见光

Unity可以剔除出被光源影响的结果

### 2.5 Multiple Directional Lights

我们在Lighting 中编写获得光照并遍历的设置光照信息的逻辑

### 2.6 Shader Loop

长度可变的循环曾经是着色器的一个问题，但现代 GPU 可以轻松处理它们，特别是当绘制调用的所有片段以相同的方式迭代相同数据时。

## 3. BRDF 双向反射分布函数

we will use BRDF （bidirectional recflectance distribution）to trade realism for performance

### 3.1 Incoming Light

express the incoming light simply
if N dot L = 1 , then they are aligned
if N dot L = -x ,then they oriented away

### 3.2 Outgoing Light

镜面反射

散射镜面反射

完美的漫反射

### 3.3 Surface Properties

我们将采用 **金属工作流程** metallic workflow
perfectly diffuse controled by metallic
perfectly mirrors controled by smoothness

BRDF 的本质 其实是 

在shader lab， hlsl 中添加对 金属度 和 光滑度 属性进行支持代码的添加

BRDF 由三个部分构成，如下
```cs
struct BRDF {  
    float3 diffuse; //漫反射  
    float3 specular;  //镜面反射
    float roughness;   // 粗擦度
};
```

### 3.4 BRDF Properties

添加BRDF结构体，将BRDF介入光照的计算

### 3.5 Reflectivity

金属度影响物体的反射率
```cs
**float** oneMinusReflectivity = 1.0 - surface.metallic;

	brdf.diffuse = surface.color * oneMinusReflectivity;
```

因为现实中完全金属的物体也会有漫反射
```csharp
#define MIN_REFLECTIVITY 0.04

**float** OneMinusReflectivity (**float** metallic) {
	**float** range = 1.0 - MIN_REFLECTIVITY;
	**return** range - metallic * range;
}
```

### 3.6 Specular Color 镜面反射颜色

以某种方式反射的光不能以另一种方式反射。这被称为**能量守恒**，即出射光的量不能超过入射光的量。这意味着**镜面反射颜色应该等于表面颜色减去漫反射颜色**。

但是我们要考虑到现实中 金属性会影响镜面反射的颜色（非金属的镜面反射应该是白色）
```csharp
brdf.specular = lerp(MIN_REFLECTIVITY, surface.color, surface.metallic);
```
为了实现更高的物理准确性和视觉真实感，对光照模型进行了更精细的调整和优化，我们采用如上方法。
因为光照和物质的相互作用并没有那么简单。“能量守恒”是过于简化的。

**PBR 的核心就在于用物理上更合理的模型来取代过去基于经验或简化假设的模型。**

>能量守恒原理是过于简化的，光和物质的相互作用还有很复杂的机制，就比如说上面所说的选择性吸收与反射。
>PBR所说的基于物理，其实也不是完全能按住物理规律去计算，而是基于物理去做更合理的计算，得到更正确的结果


>[!question] 为什么金属的镜面反射是白色？
>- **非金属的镜面反射是白色**：因为非金属的电子束缚紧密，无法选择性吸收特定波长的光来影响表面的镜面反射光，所以入射光线的所有波长都被均匀反射，呈现为白色。其固有颜色主要由内部的漫反射决定。
>- **金属的镜面反射有颜色**：因为金属拥有自由电子，这些电子会选择性地吸收和反射特定波长的光。这种选择性的反射直接影响了镜面反射的颜色，从而赋予了金属特有的外观颜色（如金的黄色、铜的红色）。
>[为什么金属性会影响镜面反射的颜色-为什么非金属的镜面反射是白色](为什么金属性会影响镜面反射的颜色-为什么非金属的镜面反射是白色.md)
>
### 3.7 Roughness 粗糙度

#TODO 复习到这里了

Roughness和smoothness 是相反关系，

根据迪士尼光照模型，在Unity引擎的Core RP 有一个函数，可以帮助计算粗糙度（Roughness）**和**光滑度（Smoothness）**参数的**非线性转换。

>[!question] 为什么不直接用 1-光滑度 来计算粗糙度？
>- `surface.smoothness` 是一个**“感知（Perceptual）”**值，更符合艺术家的直觉。
>- BRDF光照模型（尤其是GGX这类微表面模型）需要的是**“实际（Actual）”**的粗糙度值。
>- 从**感知值到实际值之间存在一个非线性的转换关系**（通常是平方），这种转换能让艺术家在调整材质参数时获得更均匀、更自然的视觉反馈。


### 3.8 View Direction

Unity的采用 约定优于配置 的机制
```csharp
float3 _WorldSpaceCameraPos;
```
所以我们在UnityInput中，声明这个变量来获取相机位置
我们需要在片元着色器中计算视线方向。
```cs
struct Varyings {
	float4 positionCS : SV_POSITION;
	float3 positionWS : VAR_POSITION;
	…
};

Varyings LitPassVertex (Attributes input) {
	…
	output.positionWS = TransformObjectToWorld(input.positionOS);
	output.positionCS = TransformWorldToHClip(output.positionWS);
	…
}
```
所以我们需要让顶点着色器传递世界空间下的顶点坐标
我们将视线方向设为Surface的属性
```cs
struct Surface {
	float3 normal;
	float3 viewDirection;
	float3 color;
	float alpha;
	float metallic;
	float smoothness;
};
```
视线方向 = 相机位置 - 顶点位置
```cs
	surface.normal = normalize(input.normalWS);
	surface.viewDirection = normalize(_WorldSpaceCameraPos - input.positionWS);
```

### 3.9 Specular Strength 镜面反射强度

镜面反射强度取决于我们的视线方向是否贴合反射光的方向
我们将使用一个复杂的公式去计算反射光强度
```cs
float Square (float v) {
	return v * v;
}

float SpecularStrength (Surface surface, BRDF brdf, Light light) {
	float3 h = SafeNormalize(light.direction + surface.viewDirection);
	float nh2 = Square(saturate(dot(surface.normal, h)));
	float lh2 = Square(saturate(dot(light.direction, h)));
	float r2 = Square(brdf.roughness);
	float d2 = Square(nh2 * (r2 - 1.0) + 1.00001);
	float normalization = brdf.roughness * 4.0 + 2.0;
	return r2 / (d2 * max(0.1, lh2) * normalization);
}
```

我的理解是这样的，先通过IncomingLight，根据光线和法线来计算入射的光的能量。
再通过BRDF，利用问题本身表面的材质、比如说金属度、光滑度，来计算漫反射和镜面反射的比率。
二者相乘得到最终反射出的光线颜色就是物体显示的颜色。

PBR的中直接光照计算的核心逻辑，是我们可以把这个过程想象成一个物理过程。
+
我们在现实中看到的物体颜色，其实就是他反射的光。所以BRDF在计算的时候，是在分配surface.color
## 4. Transparency  透明度

预乘透明度计算漫反射

漫反射 = 原漫反射 * 透明度


## 5. Shader GUI  着色器 GUI

使用Unity编辑器拓展，给材质添加预设选项