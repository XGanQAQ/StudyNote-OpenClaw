# Swagger是什么
- Swagger是一个规范和完整的框架，用于生成、描述、调用和可视化RESTful风格的Web服务。

# 如何使用Swagger

## Minimal APIs 中的Swagger示例

```csharp
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();  //启用API端点的自动发现，当然你可以不用这个方法，去手动配置Swagger生成器。

// 启用Swagger生成器
// 配置Swagger生成器，用于生成API文档。
builder.Services.AddSwaggerGen(c =>
{
     c.SwaggerDoc("v1", new OpenApiInfo {
         Title = "PizzaStore API",
         Description = "Making the Pizzas you love",
         Version = "v1" });
});

var app = builder.Build();
if (app.Environment.IsDevelopment())
{
    // 启用Swagger中间件
   app.UseSwagger();

   //允许你在浏览器中查看API文档并进行交互式测试。
   app.UseSwaggerUI(c =>
   {
      c.SwaggerEndpoint("/swagger/v1/swagger.json", "PizzaStore API V1");
   });
}

app.MapGet("/", () => "Hello World!");

app.Run();
```