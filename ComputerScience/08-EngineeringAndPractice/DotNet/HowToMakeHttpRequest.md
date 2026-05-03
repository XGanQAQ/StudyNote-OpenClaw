# 如何构建http请求
[微软官方文档](https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/console-webapiclient)

## 目标
- 发送http请求
- 反序列化（Deserialize）JSON数据
- 使用特性Attributes来进行反序列化配置

## 构建并发送Http请求
```csharp
using System.Net.Http.Headers;

using HttpClient client = new();
client.DefaultRequestHeaders.Accept.Clear();
client.DefaultRequestHeaders.Accept.Add(
    new MediaTypeWithQualityHeaderValue("application/vnd.github.v3+json"));
client.DefaultRequestHeaders.Add("User-Agent", ".NET Foundation Repository Reporter");

await ProcessRepositoriesAsync(client);

static async Task ProcessRepositoriesAsync(HttpClient client)
 {
     var json = await client.GetStringAsync(
         "https://api.github.com/orgs/dotnet/repos");

     Console.Write(json);
 }

```

## 将接收到的Json消息反序列化为对象
通过反序列化，将JSON数据转换为C#对象
```csharp
// record类型，这种声明可以自动构造出参数里的属性
public record class Repository(string name);

await using Stream stream =
    await client.GetStreamAsync("https://api.github.com/orgs/dotnet/repos");
var repositories =
    await JsonSerializer.DeserializeAsync<List<Repository>>(stream);
```

## 配置反序列化
按照默认的配置，反序列化后的属性名称与JSON数据中的属性名称一致。但是为了更好的理解，可以通过特性Attributes来进行反序列化配置。  
示例为了让反序列化后的属性名称与C#的命名规范一致，使用了`JsonPropertyName`特性。
```csharp
using System.Text.Json.Serialization;

public record class Repository(
    [property: JsonPropertyName("name")] string Name);

foreach (var repo in repositories)
   Console.Write(repo.Name);
```

## 总结
反序列化配置
```csharp
using System.Text.Json.Serialization;

//更改反序列化后对应的属性名称
public record class Repository(
    [property: JsonPropertyName("name")] string Name,
    [property: JsonPropertyName("description")] string Description,
    [property: JsonPropertyName("html_url")] Uri GitHubHomeUrl,
    [property: JsonPropertyName("homepage")] Uri Homepage,
    [property: JsonPropertyName("watchers")] int Watchers,
    [property: JsonPropertyName("pushed_at")] DateTime LastPushUtc)
{
    //添加时间戳
    public DateTime LastPush => LastPushUtc.ToLocalTime();
}
```

总流程全代码
```csharp
using System.Net.Http.Headers;
using System.Text.Json;

//发送请求
using HttpClient client = new();
client.DefaultRequestHeaders.Accept.Clear();
client.DefaultRequestHeaders.Accept.Add(
    new MediaTypeWithQualityHeaderValue("application/vnd.github.v3+json"));
client.DefaultRequestHeaders.Add("User-Agent", ".NET Foundation Repository Reporter");

//发出请求
var repositories = await ProcessRepositoriesAsync(client);

//遍历
foreach (var repo in repositories)
{
    Console.WriteLine($"Name: {repo.Name}");
    Console.WriteLine($"Homepage: {repo.Homepage}");
    Console.WriteLine($"GitHub: {repo.GitHubHomeUrl}");
    Console.WriteLine($"Description: {repo.Description}");
    Console.WriteLine($"Watchers: {repo.Watchers:#,0}");
    Console.WriteLine($"{repo.LastPush}");
    Console.WriteLine();
}

//发送请求函数
static async Task<List<Repository>> ProcessRepositoriesAsync(HttpClient client)
{
    await using Stream stream =
        await client.GetStreamAsync("https://api.github.com/orgs/dotnet/repos");
    var repositories =
        await JsonSerializer.DeserializeAsync<List<Repository>>(stream);
    return repositories ?? new();
}
```