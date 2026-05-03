---
tags:
  - "#CSharp"
---

在 C# 中，**闭包（Closure）** 是一种特殊类型的函数（或委托），它能够“捕获”其定义环境中变量的值，即使该环境在函数执行完毕后已经不存在了。简单来说，闭包记住了它被创建时的外部变量。

### 闭包的组成要素

1. **外部变量（Outer Variables）**：在闭包外部定义但在闭包内部被引用的变量。
2. **匿名函数或Lambda表达式（Anonymous Function or Lambda Expression）**：这是创建闭包的主要方式。

### 闭包的原理

当你在一个方法中定义了一个匿名方法或 Lambda 表达式，并且这个匿名方法或 Lambda 表达式引用了该方法的局部变量时，编译器会为这些被引用的局部变量创建一个特殊的类（称为“闭包类”或“显示状态机”）。这些变量不再是简单的栈变量，而是成为了这个类的字段，从而使得匿名方法或 Lambda 表达式在方法执行结束后仍然可以访问它们。

#### 问题

为什么不能直接将这个局部变量的引用直接传递给匿名方法呢？
因为局部变量的生命周期只存在于方法调用栈（stack frame）中，而闭包可能在方法返回后依然存在。  
直接传引用会导致引用一个已经销毁的栈上变量，因此编译器必须“提升变量”到堆上，通过生成捕获类来延长它的生命周期。

### C# 中闭包的常见应用场景

闭包在 C# 中非常常见，尤其是在使用 LINQ、事件处理、多线程以及需要延迟执行代码的场景中。

1. 事件处理：
    
    当你为 UI 控件添加事件处理程序时，你经常会使用闭包来捕获事件源或其他相关数据。
    
    C#
    
    ```
    public class MyForm : Form
    {
        private int clickCount = 0;
    
        public MyForm()
        {
            Button myButton = new Button();
            myButton.Text = "点击我";
            myButton.Location = new Point(10, 10);
            this.Controls.Add(myButton);
    
            // 闭包捕获了 clickCount 变量
            myButton.Click += (sender, e) =>
            {
                clickCount++; // 这里的 clickCount 就是一个被捕获的外部变量
                MessageBox.Show($"你点击了 {clickCount} 次！");
            };
        }
    }
    ```
    
2. LINQ 查询：
    
    LINQ 中的许多操作符都接受 Lambda 表达式，这些 Lambda 表达式经常会形成闭包来引用外部变量。
    
    C#
    
    ```
    public class Product
    {
        public string Name { get; set; }
        public decimal Price { get; set; }
    }
    
    public void FilterProducts()
    {
        List<Product> products = new List<Product>
        {
            new Product { Name = "苹果", Price = 5.0m },
            new Product { Name = "香蕉", Price = 3.0m },
            new Product { Name = "橙子", Price = 6.0m }
        };
    
        decimal maxPrice = 4.0m;
    
        // 闭包捕获了 maxPrice 变量
        var affordableProducts = products.Where(p => p.Price <= maxPrice);
    
        foreach (var product in affordableProducts)
        {
            Console.WriteLine($"价格合理的商品: {product.Name}");
        }
    }
    ```
    
3. 多线程/异步编程：
    
    在多线程或异步操作中，闭包可以帮助你在不同的线程上下文中访问和修改共享变量。
    
    C#
    
    ```
    public void StartBackgroundTask()
    {
        int taskId = 1001; // 外部变量
    
        Task.Run(() =>
        {
            // 闭包捕获了 taskId
            Console.WriteLine($"后台任务 {taskId} 正在执行...");
            // 模拟耗时操作
            Thread.Sleep(2000);
            Console.WriteLine($"后台任务 {taskId} 完成。");
        });
    
        // taskId 在此处仍然可用，但闭包中的是它被创建时的值（通常是引用）
        Console.WriteLine($"主线程启动了任务 {taskId}。");
    }
    ```
    

### 闭包的注意事项

1. 变量捕获方式：
    
    闭包捕获的是变量的引用，而不是变量的值（对于值类型来说，有点像引用，因为修改会影响原始变量；对于引用类型，更是捕获引用）。这意味着如果在闭包执行之前外部变量的值发生了变化，那么闭包内部看到的将是变量的最新值。
    
    C#
    
    ```
    public void IllustrateCapture()
    {
        int i = 0;
        Action[] actions = new Action[5];
    
        for (i = 0; i < 5; i++)
        {
            // 错误：这里 i 被捕获的是同一个引用，最终所有闭包都会打印 5
            // actions[i] = () => Console.WriteLine(i);
    
            // 正确：每次迭代都创建一个新的局部变量，确保每个闭包捕获到不同的值
            int temp = i;
            actions[i] = () => Console.WriteLine(temp);
        }
    
        foreach (var action in actions)
        {
            action(); // 会打印 0, 1, 2, 3, 4
        }
    }
    ```
    
    在循环中，特别需要注意变量捕获的问题。如果你直接捕获循环变量，所有闭包会共享同一个循环变量的引用，导致最终执行时它们都看到循环结束时的值。为了避免这种情况，通常会在循环内部创建一个新的局部变量来存储当前迭代的值，然后捕获这个新变量。
    
2. 性能开销：
    
    闭包会引入一些小的性能开销，因为编译器需要生成额外的类来管理捕获的变量。但在大多数情况下，这种开销是微不足道的，而且闭包带来的代码简洁性和表达力远远超过了这一点。
    
3. 生命周期：
    
    被闭包捕获的变量的生命周期会被延长，直到闭包本身不再被引用并被垃圾回收。这可能会导致一些内存泄漏，如果你创建了大量短期使用的闭包但没有正确地释放它们。
    

### 总结

C# 中的闭包是一个强大而方便的特性，它允许你在匿名方法或 Lambda 表达式中访问外部变量。理解闭包的原理和注意事项对于编写高效、正确且易于维护的 C# 代码至关重要。希望这个解释对你有帮助！如果你有其他问题，随时可以问我。