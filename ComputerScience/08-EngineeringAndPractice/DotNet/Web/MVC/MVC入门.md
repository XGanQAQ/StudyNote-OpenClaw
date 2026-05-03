## Controller控制器

### 控制器中的依赖注入
控制器类的构造函数可以通过依赖注入服务。 例如，以下构造函数将数据库上下文服务注册为依赖项服务。
```csharp
        private readonly BrainstormServerContext _context;

        public MoviesController(BrainstormServerContext context)
        {
            _context = context;
        }
```
控制器可以通过注入的数据库上下文，来操作数据库。


### 设置控制器路由
控制器中的Public方法默认是路由的，可以通过Route特性来设置路由

在Program.cs文件中
```csharp
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}"); //?代表可选
```

在控制器文件中
```csharp
[Route("api/[controller]")]
[ApiController]
public class ValuesController : ControllerBase
{
    // GET api/values
    [HttpGet]
    public ActionResult<IEnumerable<string>> Get()
    {
        return new string[] { "value1", "value2" };
    }
}
```

### 返回视图 Index方法
 如果未指定视图文件名称，则返回默认视图。 默认视图与操作方法的名称相同，在本例中为 Index。 使用视图模板 /Views/HelloWorld/Index.cshtml。
```csharp
public IActionResult Index()
{
    return View();
}
```

## Model模型

### 依赖注入数据库模型上下文
```csharp
builder.Services.AddDbContext<BrainstormServerContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("BrainstormServerContext") ?? 
    throw new InvalidOperationException("Connection string 'BrainstormServerContext' not found.")));
```


## View视图

### 菜单布局
菜单布局在 Views/Shared/_Layout.cshtml 文件中实现。
菜单布局会在所有页面显示，因此将其放在 Views/Shared 文件夹中。

### 数据传递
使用模型的方法传递数据
在控制器中使用ViewData字典传递数据
```csharp
public IActionResult Index()
{
    ViewData["Message"] = "Hello World!";
    return View();
}
```

### 

## 其他

### 配置文件
在appsetting.json中有配置数据库连接的字符串
```json 
"ConnectionStrings": {
  "BrainstormServerContext": "Server=(localdb)\\mssqllocaldb;Database=BrainstormServerContext-6f080fea-2a8a-4655-89e2-5ff06c2b07e3;Trusted_Connection=True;MultipleActiveResultSets=true"
}
```

### 数据库迁移

#### 初始迁移
```bash
Add-Migration InitialCreate
Update-Database
```

#### 迁移文件
Migrations文件夹中包含了迁移文件，可以通过迁移文件来更新数据库

### 强类型模型和@model指令
在cshtml使用强类型作为网页字段属性

