# ASP.NET Core 最小API

## 学习资源
### 微软官方文档
[Create a mini web API](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api?view=aspnetcore-8.0&tabs=visual-studio)

## 最小API基本操作

### 新建项目，使用NuGet添加依赖包
添加一下你需要用到的依赖包，比如使用数据库相关的包

### 设置数据模型，数据库上下文类


### 添加API代码


#### Map<xxx> 常用的API映射函数

#### MapGroup API
把一段URL分组，这样子就不用写老长的URL了
```csharp

// 定义Group
var todoItems = app.MapGroup("/todoitems");

//使用前
//app.MapGet("/todoitems", async (TodoDb db) =>
//    await db.Todos.ToListAsync());

//使用后
todoItems.MapGet("/", async (TodoDb db) =>
    await db.Todos.ToListAsync());

```

#### TypedResults API
使用TypedResults 替代 Results，让代码根据可测试性，并且可以自动返回类型元数据。  
方便进行单元测试

如何进行使用单元测试？  
TypedResults 是什么？一个IResult的类型工厂？

### 测试API
打开vs2022的Endpoint explorer窗口，可视化查看都有哪些API
使用.http文件发送web请求（Get，Post）

## 如何更好的组织结构
[Organizing ASP.NET Core Minimal APIs](https://www.tessferrandez.com/blog/2023/10/31/organizing-minimal-apis.html)
### 使用扩展方法来组织端点
用一个类去封装注册的方法，从而让program的代码更为简洁
```csharp
public static class TodoItemsEndpoints
{
    public static void RegisterTodoItemsEndpoints(this WebApplication app)
    {
        app.MapGet("/todoitems", async (TodoDb db) =>
            await db.Todos.ToListAsync());

        app.MapGet("/todoitems/complete", async (TodoDb db) =>
            await db.Todos.Where(t => t.IsComplete).ToListAsync());

        app.MapGet("/todoitems/{id}", async (int id, TodoDb db) =>
            await db.Todos.FindAsync(id)
                is Todo todo
                    ? Results.Ok(todo)
                    : Results.NotFound());
        ...
    }
}
```

### 使用 TypedResults 而不是 Results
还不是很清楚为什么这么做

### 将功能与端点注册分开
使用独立方法来代替lambda表达式注册端点
```csharp
app.MapGet("/todoitems/{id}", GetTodoById);

static async Task<Results<Ok<Todo>, NotFound>> GetTodoById(int id, TodoDb db) =>
    await db.Todos.FindAsync(id)
        is Todo todo
            ? TypedResults.Ok(todo)
            : TypedResults.NotFound();


app.MapGet("/todoitems", GetAllTodos);
app.MapGet("/todoitems/complete", GetCompleteTodos);
app.MapGet("/todoitems/{id}", GetTodoById);
app.MapPost("/todoitems/", CreateTodo);
app.MapPut("/todoitems/{id}", UpdateTodoById);
app.MapDelete("/todoitems/{id}", DeleteTodo);
```

### 对端点进行分组
```csharp
var todoItems = app.MapGroup("/todoitems");

todoItems.MapGet("/", GetAllTodos);
todoItems.MapGet("/complete", GetCompleteTodos);
todoItems.MapGet("/{id}", GetTodoById);
todoItems.MapPost("/", CreateTodo);
todoItems.MapPut("/{id}", UpdateTodoById);
todoItems.MapDelete("/{id}", DeleteTodo);
```

## 问题记录

1.当路由相同的时候，如果一个是Get一个是Post，浏览器是会优先发出Get指令

2.什么是路由？

3.客户端是如何决定发送什么样的请求？

4.RESTful API 是什么，为什么要有这个？

5.什么是顶级语句