在EF Core中，常用的Attribute（特性）有：

- `[Key]`：指定主键。
- `[Required]`：字段为必填。
- `[MaxLength]` / `[StringLength]`：限制字符串长度。
- `[Column]`：指定数据库列名或类型。
- `[Table]`：指定数据库表名。
- `[ForeignKey]`：指定外键。
- `[InverseProperty]`：指定导航属性的反向关系。
- `[NotMapped]`：**让EF Core忽略该属性，不在数据库中创建对应字段。**

如果你想让数据库模型忽略某个字段，只需在该属性上加上`[NotMapped]`特性。例如：

```csharp
using System.ComponentModel.DataAnnotations.Schema;

public class User
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;

    [NotMapped]
    public string TempToken { get; set; } = string.Empty; // 这个字段不会映射到数据库
}
```

这样，`TempToken`字段不会在数据库中生成对应的列。

**注意事项：**
- 需要在文件顶部添加`using System.ComponentModel.DataAnnotations.Schema;`。
- `[NotMapped]`只影响EF Core的数据库映射，不影响类的序列化或其他用途。

如需了解更多EF Core数据注解，可参考[官方文档](https://learn.microsoft.com/zh-cn/ef/core/modeling/entity-properties?tabs=data-annotations)。