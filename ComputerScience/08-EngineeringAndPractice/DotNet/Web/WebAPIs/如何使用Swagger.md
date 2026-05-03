## 如何使用Swagger

### 环境准备
```bash
dotnet --list-sdks #查看已安装的SDK，确保你已经安装.NET8.0或者更高版本

dotnet add package Swashbuckle.AspNetCore --version 6.5.0 #安装 Swashbuckle 包
```

### 映射对象/数据模型
新建文件
```csharp
namespace PizzaStore.Models 
{
    public class Pizza
    {
          public int Id { get; set; }
          public string? Name { get; set; }
          public string? Description { get; set; }
    }
}
```

### Program中配置Swagger
```csharp
//引入Swagger
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

//配置Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
     c.SwaggerDoc("v1", new OpenApiInfo {
         Title = "PizzaStore API",
         Description = "Making the Pizzas you love",
         Version = "v1" });
});


var app = builder.Build();

//配置Swagger
if (app.Environment.IsDevelopment())
{
   app.UseSwagger();
   app.UseSwaggerUI(c =>
   {
      c.SwaggerEndpoint("/swagger/v1/swagger.json", "PizzaStore API V1");
   });
}

app.MapGet("/", () => "Hello World!");

app.Run();
```