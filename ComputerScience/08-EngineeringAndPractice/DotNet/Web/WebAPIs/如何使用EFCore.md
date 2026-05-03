## 如何使用EFCore

### 安装EFCore包
```shell
dotnet --list-sdks #查看已安装的SDK，确保你已经安装.NET8.0或者更高版本

#安装 EFCore 包
#这个是针对内存数据库的，如果你想使用SQLite数据库，可以使用Microsoft.EntityFrameworkCore.Sqlite
dotnet add package Microsoft.EntityFrameworkCore.InMemory --version 8.0
```

### 定义实体类、数据库上下文类
```csharp
namespace PizzaStore.Models 
{
  public class Pizza
  {
      public int Id { get; set; }
      public string? Name { get; set; }
      public string? Description { get; set; }
  }

  class PizzaDb : DbContext
  {
      public PizzaDb(DbContextOptions options) : base(options) { }
      public DbSet<Pizza> Pizzas { get; set; } = null!;
  }
}
```

### 在Program中配置EFCore
```csharp
//引入EFCore
using Microsoft.EntityFrameworkCore; 

//配置EFCore,使用内存数据库,数据库名为items
//如果你有使用Swagger应该注意，此配置应该在AddSwaggerGen之前
builder.Services.AddDbContext<PizzaDb>(options => options.UseInMemoryDatabase("items")); 
```

### 基本的CRUD操作
```csharp
//查找
var pizzas = await db.Pizzas.ToListAsync();
//添加
await db.pizzas.AddAsync(
    new Pizza { ID = 1, Name = "Pepperoni", Description = "The classic pepperoni pizza" });
//删除
var pizza = await db.pizzas.FindAsync(id);
if (pizza is null)
{
    //Handle error
}
db.pizzas.Remove(pizza);
//更新
int id = 1;
var updatepizza = new Pizza { Name = "Pineapple", Description = "Ummmm?" };
var pizza = await db.pizzas.FindAsync(id);
if (pizza is null)
{
    //Handle error
}
pizza.Desription = updatepizza.Description;
pizza.Name = updatepizza.Name;
await db.SaveChangesAsync();
```

### 更换数据库
```bash
#安装SQLite数据库包 你需要的对应数据库包
dotnet add package Microsoft.EntityFrameworkCore.Sqlite --version 8.0
#EF Core工具 用于生成数据库迁移
dotnet tool install --global dotnet-ef
#包含 EF Core 用于创建数据库的所有设计时逻辑
dotnet add package Microsoft.EntityFrameworkCore.Design --version 8.0
```

添加连接字符串
```csharp
var connectionString = builder.Configuration.GetConnectionString("Pizzas") ?? "Data Source=Pizzas.db";

builder.Services.AddSqlite<PizzaDb>(connectionString); //使用SQLite数据库
```

使用EF Core工具生成数据库迁移
```bash
dotnet ef migrations add InitialCreate #生成数据库迁移

dotnet ef database update #更新数据库
```
你可以看到新创建的 Pizzas.db 文件