以下是 **ASP.NET Core** 的层级架构，从底层基础设施到应用逻辑逐层展开，帮助理解其核心组件的协作关系：

---

### 1. **宿主层（Host Layer）**  
**作用**：初始化应用程序的运行时环境，配置依赖注入、配置系统和日志。  
**核心组件**：  
• **`IHostBuilder` / `WebHostBuilder`**：构建宿主环境（如 `Startup` 类加载）。  
• **`IHost` / `WebHost`**：管理应用生命周期（启动、停止）。  
• **`Startup` 类**：定义 `ConfigureServices`（服务注册）和 `Configure`（中间件配置）。  

**示例代码**：  
```csharp
public class Program {
    public static void Main(string[] args) => 
        CreateHostBuilder(args).Build().Run();

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder => {
                webBuilder.UseStartup<Startup>();
            });
}
```

---

### 2. **中间件管道（Middleware Pipeline）**  
**作用**：处理 HTTP 请求和响应的流水线，按注册顺序执行中间件。  
**核心组件**：  
• **中间件（Middleware）**：  
  • **内置中间件**：`UseRouting()`、`UseAuthentication()`、`UseStaticFiles()`。  
  • **自定义中间件**：通过 `app.Use()` 或 `IMiddleware` 接口实现。  
• **终结点路由（Endpoint Routing）**：`UseEndpoints()` 定义 MVC 控制器、Razor Pages 或 SignalR 的终结点。  

**请求处理流程**：  
```plaintext
客户端请求 → Kestrel → 中间件1 → 中间件2 → ... → 终结点（控制器） → 逆向中间件 → 响应
```

---

### 3. **应用模型层（Application Model Layer）**  
**作用**：定义处理业务逻辑的编程模型。  
**核心模型**：  
• **MVC（Model-View-Controller）**：  
  • **Controller**：处理请求逻辑，返回 `IActionResult`（如 `View()` 或 `Json()`）。  
  • **Model**：数据实体或 DTO（数据传输对象）。  
  • **View**：Razor 视图生成 HTML。  
• **Razor Pages**：基于页面的模型，将 UI 和逻辑封装在 `.cshtml` 文件中。  
• **Web API**：通过 `[ApiController]` 属性返回 JSON/XML 数据。  
• **Minimal APIs**（.NET 6+）：极简语法定义 API 终结点。  

**示例**：  
```csharp
// MVC 控制器
public class HomeController : Controller {
    public IActionResult Index() => View();
}

// Minimal API
app.MapGet("/hello", () => "Hello World!");
```

---

### 4. **服务与依赖注入层（Dependency Injection Layer）**  
**作用**：解耦组件依赖，管理服务生命周期。  
**核心概念**：  
• **服务注册**：在 `Startup.ConfigureServices` 中通过 `services.AddXxx()` 注册服务。  
• **生命周期**：  
  • **Transient**：每次请求创建新实例。  
  • **Scoped**：同一请求内共享实例。  
  • **Singleton**：全局单例。  
• **内置服务**：`ILogger<T>`、`IConfiguration`、`IWebHostEnvironment`。  

**示例**：  
```csharp
public void ConfigureServices(IServiceCollection services) {
    services.AddScoped<IMyService, MyService>();  // 注册作用域服务
    services.AddControllers();                    // 注册 MVC 控制器
}
```

---

### 5. **配置系统（Configuration System）**  
**作用**：统一管理应用配置（如数据库连接、密钥）。  
**核心机制**：  
• **多源配置**：支持 JSON 文件（`appsettings.json`）、环境变量、命令行参数等。  
• **强类型绑定**：通过 `IConfiguration` 接口绑定到 POCO 类。  

**示例**：  
```json
// appsettings.json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=mydb;"
  }
}
```

```csharp
// 绑定到类
public class DatabaseSettings {
    public string ConnectionString { get; set; }
}

// 在 Startup 中配置
services.Configure<DatabaseSettings>(Configuration.GetSection("Database"));
```

---

### 6. **数据访问层（Data Access Layer）**  
**作用**：与数据库或外部服务交互。  
**核心工具**：  
• **Entity Framework Core**：ORM 框架，支持 Code First 或 Database First。  
• **Dapper**：轻量级 SQL 映射器。  
• **仓储模式（Repository Pattern）**：封装数据访问逻辑。  

**示例**：  
```csharp
// 使用 EF Core
public class AppDbContext : DbContext {
    public DbSet<User> Users { get; set; }
}

// 在控制器中注入
public class UserController : Controller {
    private readonly AppDbContext _context;
    public UserController(AppDbContext context) => _context = context;
}
```

---

### 7. **安全层（Security Layer）**  
**作用**：实现身份验证、授权和数据保护。  
**核心机制**：  
• **认证（Authentication）**：Cookie、JWT、OAuth（如 `AddAuthentication()`）。  
• **授权（Authorization）**：基于策略（Policy）或角色（Role）的权限控制。  
• **数据保护（Data Protection）**：加密敏感数据（如 `IDataProtector`）。  

**示例**：  
```csharp
// 配置 JWT 认证
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options => {
        options.TokenValidationParameters = new TokenValidationParameters {
            ValidateIssuer = true,
            ValidIssuer = "my-issuer",
            ValidateAudience = true,
            ValidAudience = "my-audience",
            ValidateLifetime = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("my-secret-key"))
        };
    });
```

---

### 8. **跨领域组件（Cross-Cutting Components）**  
**作用**：支撑应用的非功能性需求。  
**关键模块**：  
• **日志（Logging）**：通过 `ILogger<T>` 记录日志，支持多种提供程序（Console、File、Azure）。  
• **健康检查（Health Checks）**：`AddHealthChecks()` 监控应用状态。  
• **实时通信（Real-Time）**：通过 SignalR 实现 WebSocket 双向通信。  

---

### 总结：ASP.NET Core 架构的层级协作  
1. **宿主启动**：构建运行时环境，加载配置和服务。  
2. **中间件处理**：按顺序处理请求，路由到终结点。  
3. **应用模型**：执行控制器或 Razor Page 逻辑。  
4. **数据与安全**：通过依赖注入访问数据，认证授权保障安全。  
5. **响应返回**：逆向中间件处理响应，返回客户端。  

通过这种分层架构，ASP.NET Core 实现了 **高内聚低耦合** 的设计，使开发者能够灵活选择组件（如替换 ORM 或认证方案），同时保持高性能和跨平台能力。