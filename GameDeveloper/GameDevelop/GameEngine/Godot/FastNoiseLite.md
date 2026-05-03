
在 Godot 中使用 `FastNoiseLite` 生成噪声图时，有许多参数可以调整，以控制噪声的外观和行为。以下是噪声图的基本设置参数及其属性的详细说明：

---

### 1. **噪声类型 (`noise_type`)**
- **作用**: 决定噪声的生成算法。
- **可选值**:
  - `FastNoiseLite.TYPE_PERLIN`: Perlin 噪声，平滑且连续，适合自然地形。
  - `FastNoiseLite.TYPE_SIMPLEX`: Simplex 噪声，计算效率高，适合实时应用。
  - `FastNoiseLite.TYPE_CELLULAR`: 细胞噪声，生成类似细胞或瓦片的图案。
  - `FastNoiseLite.TYPE_VALUE`: 值噪声，生成块状噪声。
  - `FastNoiseLite.TYPE_VALUE_CUBIC`: 立方值噪声，平滑的值噪声。
- **默认值**: `FastNoiseLite.TYPE_SIMPLEX`

---

### 2. **种子 (`seed`)**
- **作用**: 控制噪声的随机性。相同的种子会生成相同的噪声图。
- **类型**: 整数 (`int`)
- **默认值**: 随机值

---

### 3. **频率 (`frequency`)**
- **作用**: 控制噪声的细节密度。频率越高，噪声变化越快。
- **类型**: 浮点数 (`float`)
- **默认值**: `0.01`
- **建议范围**: `0.001`（低频，平滑）到 `0.1`（高频，细节丰富）

---

### 4. **倍频 (`fractal_octaves`)**
- **作用**: 控制噪声的叠加层数。每一层称为一个“倍频”，增加倍频会增加噪声的细节。
- **类型**: 整数 (`int`)
- **默认值**: `3`
- **建议范围**: `1`（简单噪声）到 `8`（复杂噪声）

---

### 5. **间隙度 (`fractal_lacunarity`)**
- **作用**: 控制每一层噪声频率的增长速度。值越高，高频噪声（细节）越集中在某些区域。
- **类型**: 浮点数 (`float`)
- **默认值**: `2.0`
- **建议范围**: `1.5`（平缓）到 `2.5`（陡峭）

---

### 6. **增益 (`fractal_gain`)**
- **作用**: 控制每一层噪声振幅的衰减速度。值越高，高频噪声的振幅越大。
- **类型**: 浮点数 (`float`)
- **默认值**: `0.5`
- **建议范围**: `0.3`（快速衰减）到 `0.7`（缓慢衰减）

---

### 7. **分形类型 (`fractal_type`)**
- **作用**: 控制分形噪声的生成方式。
- **可选值**:
  - `FastNoiseLite.FRACTAL_NONE`: 无分形噪声。
  - `FastNoiseLite.FRACTAL_FBM`: 分形布朗运动（FBM），平滑且连续。
  - `FastNoiseLite.FRACTAL_RIDGED`: 脊状分形，生成类似山脉的图案。
  - `FastNoiseLite.FRACTAL_PING_PONG`: 乒乓分形，生成来回振荡的图案。
- **默认值**: `FastNoiseLite.FRACTAL_FBM`

---

### 8. **细胞距离函数 (`cellular_distance_func`)**
- **作用**: 仅适用于细胞噪声，控制细胞之间的距离计算方式。
- **可选值**:
  - `FastNoiseLite.DISTANCE_EUCLIDEAN`: 欧几里得距离。
  - `FastNoiseLite.DISTANCE_MANHATTAN`: 曼哈顿距离。
  - `FastNoiseLite.DISTANCE_HYBRID`: 混合距离。
- **默认值**: `FastNoiseLite.DISTANCE_EUCLIDEAN`

---

### 9. **细胞返回类型 (`cellular_return_type`)**
- **作用**: 仅适用于细胞噪声，控制返回的细胞值类型。
- **可选值**:
  - `FastNoiseLite.RETURN_CELL_VALUE`: 返回细胞的值。
  - `FastNoiseLite.RETURN_DISTANCE`: 返回距离。
  - `FastNoiseLite.RETURN_DISTANCE2`: 返回第二近的距离。
  - `FastNoiseLite.RETURN_DISTANCE2_ADD`: 返回距离和第二近距离的和。
  - `FastNoiseLite.RETURN_DISTANCE2_SUB`: 返回距离和第二近距离的差。
  - `FastNoiseLite.RETURN_DISTANCE2_MUL`: 返回距离和第二近距离的积。
  - `FastNoiseLite.RETURN_DISTANCE2_DIV`: 返回距离和第二近距离的商。
- **默认值**: `FastNoiseLite.RETURN_CELL_VALUE`

---

### 10. **偏移 (`offset`)**
- **作用**: 控制噪声图的偏移量，可以用于平移噪声图。
- **类型**: `Vector3`
- **默认值**: `Vector3(0, 0, 0)`

---

### 11. **域变形 (`domain_warp_enabled`)**
- **作用**: 启用域变形，可以使噪声图产生扭曲效果。
- **类型**: 布尔值 (`bool`)
- **默认值**: `false`

---

### 12. **域变形类型 (`domain_warp_type`)**
- **作用**: 控制域变形的类型。
- **可选值**:
  - `FastNoiseLite.DOMAIN_WARP_SIMPLEX`: Simplex 域变形。
  - `FastNoiseLite.DOMAIN_WARP_SIMPLEX_REDUCED`: 简化 Simplex 域变形。
  - `FastNoiseLite.DOMAIN_WARP_BASIC_GRID`: 基本网格域变形。
- **默认值**: `FastNoiseLite.DOMAIN_WARP_SIMPLEX`

---

### 13. **域变形幅度 (`domain_warp_amplitude`)**
- **作用**: 控制域变形的强度。
- **类型**: 浮点数 (`float`)
- **默认值**: `1.0`

---

### 14. **域变形频率 (`domain_warp_frequency`)**
- **作用**: 控制域变形的细节密度。
- **类型**: 浮点数 (`float`)
- **默认值**: `0.01`

---

### 15. **域变形倍频 (`domain_warp_fractal_octaves`)**
- **作用**: 控制域变形的叠加层数。
- **类型**: 整数 (`int`)
- **默认值**: `3`

---

### 16. **域变形间隙度 (`domain_warp_fractal_lacunarity`)**
- **作用**: 控制域变形每一层频率的增长速度。
- **类型**: 浮点数 (`float`)
- **默认值**: `2.0`

---

### 17. **域变形增益 (`domain_warp_fractal_gain`)**
- **作用**: 控制域变形每一层振幅的衰减速度。
- **类型**: 浮点数 (`float`)
- **默认值**: `0.5`

---

### 示例代码
以下是一个完整的噪声图设置示例：

```gdscript
extends Node2D

var noise = FastNoiseLite.new()

func _ready():
    # 基本设置
    noise.noise_type = FastNoiseLite.TYPE_PERLIN
    noise.seed = 12345
    noise.frequency = 0.02
    
    # 分形设置
    noise.fractal_octaves = 4
    noise.fractal_lacunarity = 2.0
    noise.fractal_gain = 0.5
    noise.fractal_type = FastNoiseLite.FRACTAL_FBM
    
    # 域变形设置
    noise.domain_warp_enabled = true
    noise.domain_warp_type = FastNoiseLite.DOMAIN_WARP_SIMPLEX
    noise.domain_warp_amplitude = 1.0
    noise.domain_warp_frequency = 0.01
    noise.domain_warp_fractal_octaves = 3
    noise.domain_warp_fractal_lacunarity = 2.0
    noise.domain_warp_fractal_gain = 0.5
    
    # 获取噪声值
    var x = 50
    var y = 50
    var noise_value = noise.get_noise_2d(x, y)
    print("Noise value at (", x, ", ", y, "): ", noise_value)
```

---

### 总结
以上是 `FastNoiseLite` 的基本参数及其作用。通过调整这些参数，你可以生成各种类型的噪声图，用于地形生成、纹理生成、程序化生成等场景。根据你的需求，灵活调整这些参数即可！