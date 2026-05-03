**Fluent API** 是 Entity Framework Core 中的一种用于配置模型与数据库映射的方式。它是一种基于代码的配置方法，提供了比数据注解（Data Annotations）更强大和灵活的配置选项。使用 Fluent API，你可以在 `OnModelCreating` 方法中，通过方法链式调用的方式来配置实体类的属性、关系、表、约束等映射规则。

### 为什么使用 Fluent API？

- **灵活性更高**：Fluent API 提供比数据注解更多的配置选项，特别是在处理复杂映射和关系时。
- **代码集中管理**：Fluent API 将所有配置集中在 `DbContext` 的 `OnModelCreating` 方法中，使得数据库配置更易于管理。
- **避免与业务逻辑冲突**：数据注解会直接嵌入到实体类中，而 Fluent API 配置是在 `DbContext` 中定义，避免了与业务逻辑的耦合。

### 1. 配置实体的属性

Fluent API 可以用来配置实体的属性，如设置属性为必填、指定最大长度、设置默认值等。

#### 例子：配置属性

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<User>()
        .Property(u => u.Name)
        .IsRequired()  // 设置 Name 为必填
        .HasMaxLength(100);  // 设置 Name 的最大长度为 100

    modelBuilder.Entity<User>()
        .Property(u => u.Email)
        .HasDefaultValue("example@example.com");  // 设置 Email 默认值
}
```

### 2. 配置表和列名

你可以使用 Fluent API 来指定数据库中的表名和列名，允许你控制数据库中的结构。

#### 例子：设置表名和列名

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 设置表名
    modelBuilder.Entity<User>()
        .ToTable("tbl_Users");

    // 设置列名
    modelBuilder.Entity<User>()
        .Property(u => u.Name)
        .HasColumnName("FullName");
}
```

### 3. 配置关系（例如：一对多、多对多）

Fluent API 允许你配置实体之间的关系，例如一对多、多对多关系等。

#### 例子：一对多关系

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 配置一对多关系
    modelBuilder.Entity<Order>()
        .HasOne(o => o.Customer)  // 每个 Order 有一个 Customer
        .WithMany(c => c.Orders)  // 每个 Customer 可以有多个 Order
        .HasForeignKey(o => o.CustomerId);  // 外键
}
```

#### 例子：多对多关系

在 EF Core 5 及以后版本，Fluent API 还可以用来配置多对多关系。

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<StudentCourse>()
        .HasKey(sc => new { sc.StudentId, sc.CourseId });  // 配置复合主键

    modelBuilder.Entity<StudentCourse>()
        .HasOne(sc => sc.Student)
        .WithMany(s => s.StudentCourses)
        .HasForeignKey(sc => sc.StudentId);

    modelBuilder.Entity<StudentCourse>()
        .HasOne(sc => sc.Course)
        .WithMany(c => c.StudentCourses)
        .HasForeignKey(sc => sc.CourseId);
}
```

### 4. 配置主键和索引

Fluent API 可以用来配置主键、复合主键、唯一索引等。

#### 例子：配置主键

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 配置主键
    modelBuilder.Entity<User>()
        .HasKey(u => u.Id);
}
```

#### 例子：配置复合主键

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 配置复合主键
    modelBuilder.Entity<Order>()
        .HasKey(o => new { o.OrderId, o.ProductId });
}
```

#### 例子：配置索引

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 配置索引
    modelBuilder.Entity<User>()
        .HasIndex(u => u.Email)  // 为 Email 字段创建索引
        .IsUnique();  // 设置为唯一索引
}
```

### 5. 配置约束（如：非空、唯一等）

Fluent API 还可以用来配置列的约束，例如设置属性为非空、唯一、或者设置数据类型。

#### 例子：配置唯一约束

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    // 设置 Email 字段为唯一
    modelBuilder.Entity<User>()
        .HasIndex(u => u.Email)
        .IsUnique();
}
```

#### 例子：配置非空字段

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<User>()
        .Property(u => u.Name)
        .IsRequired();  // 设置 Name 字段为非空
}
```

### 6. 配置删除行为

Fluent API 可以配置实体之间的删除行为，例如级联删除、限制删除等。

#### 例子：级联删除

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<Order>()
        .HasOne(o => o.Customer)
        .WithMany(c => c.Orders)
        .OnDelete(DeleteBehavior.Cascade);  // 设置级联删除
}
```

#### 例子：限制删除（禁止级联删除）

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<Order>()
        .HasOne(o => o.Customer)
        .WithMany(c => c.Orders)
        .OnDelete(DeleteBehavior.Restrict);  // 禁止级联删除
}
```

### 7. 配置枚举属性

Fluent API 还可以用于配置枚举类型字段的存储方式（存储为整数还是字符串等）。

#### 例子：枚举存储为字符串

```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    base.OnModelCreating(modelBuilder);

    modelBuilder.Entity<User>()
        .Property(u => u.Status)
        .HasConversion<string>();  // 将枚举存储为字符串
}
```

### 总结

- **Fluent API** 是 Entity Framework Core 中用于配置数据库模型与数据库映射的一种代码配置方式，通常在 `DbContext` 类的 `OnModelCreating` 方法中使用。
- **Fluent API** 的优势在于其高灵活性，能够处理复杂的配置场景，如一对多、多对多关系、复杂的属性配置、索引和约束、删除行为等。
- Fluent API 相对于数据注解来说更强大，尤其是在处理复杂映射时，数据注解的功能有限。

Fluent API 让你可以用更细粒度的控制去定义实体和数据库之间的映射关系，使得代码更加清晰且易于维护。