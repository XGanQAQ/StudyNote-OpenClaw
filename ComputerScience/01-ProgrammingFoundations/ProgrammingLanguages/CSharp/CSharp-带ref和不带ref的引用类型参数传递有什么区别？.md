ref 传递的是引用本身
不带ref 传递的是引用的副本

这俩个有什么区别？
示例如下
```cs

public class MyProgram  
{  
    public static void Main(string[] args)  
    {        MyClass myClass = new MyClass(){name="111"};  
        MyClass myClass2 = new MyClass(){name="222"};  
        PrintName(myClass);  
        PrintName(ref myClass2);  
        PrintName(myClass);  
        PrintName(ref myClass2);  
    }  
    private static void PrintName(MyClass myClass)  
    {        Console.WriteLine(myClass.name);  
        myClass = new MyClass(){name = "new class"};  
    }  
    private static void PrintName(ref MyClass myClass)  
    {        Console.WriteLine(myClass.name);  
        myClass = new MyClass(){name = "new class"};  
    }}  
  
public class MyClass  
{  
    public string name;  
}

//输出结果
//111
//222
//111
//new class

```

你可以在方法内通过地址副本去修改对象（因为它们都指向同一个地方），但你不能通过给参数重新赋值来改变原始变量所存储的地址