---
tags:
  - "#CSharp"
---

## 定义函数的工具

### Method 方法

### Extension 扩展方法
扩展方法本质是一个语法糖，利用它可以构造简洁清晰的代码
### Delegate 委托
委托是一种类型，安全的封装了一个方法
- Func<T1,T2,T3,TResult> 
	- 带返回结果
	- 灵活
- Action<T1,T2> 
	- 不带结果
	- 隔离执行操作和带副作用的代码
- Predicate<T1,TBool> 
	- 接受一个参数，返回一个Bool
	- 用于编写自定义过滤数据

### Lambda 表达式
短函数、匿名函数，作为参数

## 实例参考

传递参数对List进行过滤
```csharp
protected List<Project> FilterProjectWithTag(List<Project> projects, Func<Project, bool> predicate)
{
    if (predicate == null)
        return projects;
    return projects.Where(predicate).ToList();
}
```