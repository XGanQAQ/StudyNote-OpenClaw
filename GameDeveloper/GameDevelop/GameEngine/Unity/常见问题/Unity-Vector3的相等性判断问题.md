# Unity Vector3 相等性判断 快速笔记

## 1. 结论先行
- **别手写 `a.x==b.x && a.y==b.y && a.z==b.z`**  
- **直接用 `a == b` 或 `a.Equals(b)`**  
  Unity 已内置 **1e-5 容忍度** 的近似相等。

## 2. 源码实现（2020.3+）
```csharp
public static bool operator ==(Vector3 lhs, Vector3 rhs){
    float sqrmag = (lhs - rhs).sqrMagnitude;   // 避免开方
    return sqrmag < 9.999999E-11f;             // (1e-5)²
}
```
- 阈值固定 **1e-5**（与坐标量级无关）
- 接口：  
  `==` / `Equals(object)` / `Equals(Vector3)` 都走同一逻辑

## 3. 用法示例
```csharp
Vector3 a = new Vector3(1, 2, 3);
Vector3 b = new Vector3(1, 2.000009f, 3);

bool eq  = (a == b);        // true
bool eq2 = a.Equals(b);     // true
```

## 4. 需要不同容忍度时
```csharp
float tol = 0.001f;
bool looseEq = (a - b).sqrMagnitude < tol * tol;
```

## 5. 性能提示
- 优先用 **sqrMagnitude** 而不是 `Vector3.Distance`（省掉一次开方）
- 热路径里避免重复 `==` 产生多余函数调用，可手动展开

## 6. 常见坑
| 场景 | 表现 | 解决 |
|---|---|---|
| 很大/很小坐标 | 1e-5 可能过严/过松 | 自定义容忍度或改用相对误差 |
| 网络同步/哈希 | 需要逐位一致 | 先量化到整数再比，或不用 `==` |

------------------------------------------------
一句话背下来：  
**Unity 的 Vector3 已经帮你包好浮点误差——直接 `==` 就行，特殊精度再自己算 sqrMagnitude。**