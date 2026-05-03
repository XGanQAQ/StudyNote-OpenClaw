[Creating a Mesh](https://catlikecoding.com/unity/tutorials/procedural-meshes/creating-a-mesh/)

## 简单程序网格组件

>[!question] 法线贴图如何通过切线空间（Tangent Space）将法线信息转换到世界空间的？
>[法线贴图如何通过切线空间（Tangent Space）将法线信息转换到世界空间的？](法线贴图如何通过切线空间（Tangent%20Space）将法线信息转换到世界空间的？.md)

利用 MeshFilter 和 MeshRenderer 来渲染网格

### 源代码

```csharp
using System.Collections;  
using System.Collections.Generic;  
using UnityEngine;  
  
[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]  
public class SimpleProceduralMesh : MonoBehaviour  
{  
    void OnEnable()  
    {        
	    var mesh = new Mesh  
        {  
            name = "Procedural Mesh"  
        };  
		//顶点
        mesh.vertices = new Vector3[]  
        {            Vector3.zero, Vector3.right, Vector3.up, new Vector3(1f, 1f)  
        };  
        //三角形索引
        mesh.triangles = new int[]  
        {            0, 2, 1, 1, 2, 3  
        };  
		//法线
        mesh.normals = new Vector3[]  
        {            Vector3.back, Vector3.back, Vector3.back, Vector3.back  
        };  
		//切线
        mesh.tangents = new Vector4[]  
        {            new Vector4(1f, 0f, 0f, -1f),  
            new Vector4(1f, 0f, 0f, -1f),  
            new Vector4(1f, 0f, 0f, -1f),  
            new Vector4(1f, 0f, 0f, -1f)  
        };  
        //纹理坐标
        mesh.uv = new Vector2[]  
        {            Vector2.zero, Vector2.right, Vector2.up, Vector2.one  
        };  
        GetComponent<MeshFilter>().mesh = mesh;  
    }}
```

## Advanced Mesh API 高级网格API

这种方式更为繁琐，但是更接近底层API，是Unity对于图形API的一层封装，比起简单调用的方法性能优化和自定义程度更高。

>[!question] Burst是什么？
>Unity 的 **Burst 编译器**（通常简称为 Burst）是一个高性能的编译器，它能将你的 C# 代码转换为高度优化的机器码。它专门为 Unity 的**Job System**（Job 系统）和**Entities**（实体组件系统，ECS）设计，旨在充分利用现代 CPU 的多核架构和 SIMD（单指令多数据）指令集。

>When we assign data to a mesh via the simple API Unity has to copy and convert everything to the mesh's native memory at some point. The advanced API allows us to work directly in the native memory format of the mesh, skipping conversion.
>当我们通过简单 API 为网格分配数据时，Unity 必须在某个时刻将所有内容复制并转换到网格的原生内存中。高级 API 允许我们直接使用网格的原生内存格式，跳过转换步骤。这意味着我们必须了解网格数据的布局方式。

>Each vertex of our mesh has four attributes: a position, a normal, a tangent, and a set of texture ?coordinates.
>我们网格的每个顶点都有四个属性：位置、法线、切线和一组纹理坐标。

>When we create a mesh this way Unity doesn't automatically calculate its bounds. However, Unity does calculate the bounds of a submesh, which are needed in some cases. This requires checking all vertices of the submesh. We can avoid all that work be providing the correct bounds ourselves, by setting the `bounds` property of the submesh descriptor that we pass to `SetSubMesh`. We should also set its `vertexCount` property.
>当我们以这种方式创建网格时，Unity 不会自动计算其边界。但是，Unity 会计算子网格的边界，这在某些情况下是必要的。这需要检查子网格的所有顶点。我们可以自己设置正确的边界，方法是设置传递给 `SetSubMesh` 子网格描述符的 `bounds` 属性。我们还应该设置它的 `vertexCount` 属性。
### 源代码
```csharp
using System.Collections;  
using System.Collections.Generic;  
using UnityEngine;  
using Unity.Collections;  
using UnityEngine.Rendering;  
using Unity.Mathematics;  
using static Unity.Mathematics.math;  
  
namespace ProceduralMesh  
{  
    [RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]  
    public class AdvancedMultiStreamProceduralMesh : MonoBehaviour  
    {  
        void OnEnable()  
        {            int vertexAttributeCount = 4;  
            int vertexCount = 4;  
            int triangleIndexCount = 6;  
  
            Mesh.MeshDataArray meshDataArray = Mesh.AllocateWritableMeshData(1);  
            Mesh.MeshData meshData = meshDataArray[0];  
  
            var vertexAttributes = new NativeArray<VertexAttributeDescriptor>(  
                vertexAttributeCount, Allocator.Temp, NativeArrayOptions.UninitializedMemory  
            );  
            vertexAttributes[0] = new VertexAttributeDescriptor(dimension: 3);  
            vertexAttributes[1] = new VertexAttributeDescriptor(  
                VertexAttribute.Normal, dimension: 3, stream: 1  
            );  
            vertexAttributes[2] = new VertexAttributeDescriptor(  
                VertexAttribute.Tangent, dimension: 4, stream: 2  
            );  
            vertexAttributes[3] = new VertexAttributeDescriptor(  
                VertexAttribute.TexCoord0, dimension: 2, stream: 3  
            );  
            meshData.SetVertexBufferParams(vertexCount, vertexAttributes);  
            vertexAttributes.Dispose();  
            NativeArray<float3> positions = meshData.GetVertexData<float3>();  
            positions[0] = 0f;  
            positions[1] = right();  
            positions[2] = up();  
            positions[3] = float3(1f, 1f, 0f);  
  
            NativeArray<float3> normals = meshData.GetVertexData<float3>(1);  
            normals[0] = normals[1] = normals[2] = normals[3] = back();  
  
            NativeArray<float4> tangents = meshData.GetVertexData<float4>(2);  
            tangents[0] = tangents[1] = tangents[2] = tangents[3] = float4(1f, 0f, 0f, -1f);  
  
            NativeArray<float2> texCoords = meshData.GetVertexData<float2>(3);  
            texCoords[0] = 0f;  
            texCoords[1] = float2(1f, 0f);  
            texCoords[2] = float2(0f, 1f);  
            texCoords[3] = 1f;  
  
            meshData.SetIndexBufferParams(triangleIndexCount, IndexFormat.UInt16);  
            NativeArray<ushort> triangleIndices = meshData.GetIndexData<ushort>();  
            triangleIndices[0] = 0;  
            triangleIndices[1] = 2;  
            triangleIndices[2] = 1;  
            triangleIndices[3] = 1;  
            triangleIndices[4] = 2;  
            triangleIndices[5] = 3;  
  
            var bounds = new Bounds(new Vector3(0.5f, 0.5f), new Vector3(1f, 1f));  
  
            meshData.subMeshCount = 1;  
            meshData.SetSubMesh(0, new SubMeshDescriptor(0, triangleIndexCount) {  
                bounds = bounds,  
                vertexCount = vertexCount  
            }, MeshUpdateFlags.DontRecalculateBounds);  
            var mesh = new Mesh  
            {  
                bounds = bounds,  
                name = "Procedural Mesh"  
            };  
            Mesh.ApplyAndDisposeWritableMeshData(meshDataArray, mesh);  
            GetComponent<MeshFilter>().mesh = mesh;  
        }    }}
```

![](AdvancedAPI.png)

## 总结

Simple Procedural Mesh 更方便，但是需要有一定的额外内存开销。
Advanced Mesh API 更繁琐（很类似我在使用OpenGL的时候进行的操作模式），但是自定义程度高，可以做更多的优化。