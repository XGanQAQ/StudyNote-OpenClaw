## 核心思想

- **将“对对象执行的操作”从对象结构中分离**
    
- 在**不修改已有类**的情况下，新增对这些对象的操作
    
- 适用于：**对象结构稳定，操作经常变化**
    
- 通过 **Accept + Visit（双重分发）** 实现按“对象类型 × 操作类型”区分行为
    

---

## 代码示例（简化 C#）

```csharp
// Element
interface IElement {
    void Accept(IVisitor visitor);
}

// Concrete Element
class A : IElement {
    public void Accept(IVisitor visitor) => visitor.Visit(this);
}

class B : IElement {
    public void Accept(IVisitor visitor) => visitor.Visit(this);
}

// Visitor
interface IVisitor {
    void Visit(A a);
    void Visit(B b);
}

// Concrete Visitor
class PrintVisitor : IVisitor {
    public void Visit(A a) => Console.WriteLine("A");
    public void Visit(B b) => Console.WriteLine("B");
}
```

使用：

```csharp
IVisitor visitor = new PrintVisitor();
element.Accept(visitor);
```

---

## 适用场景

**适合**

- 编译器 / AST 遍历
    
- 复杂规则结算、统计、分析
    
- 数据结构稳定，但操作不断增加的系统
    

**不适合**

- 元素类型经常变动
    
- 逻辑非常简单的业务代码
    
- Unity 日常 MonoBehaviour 脚本
    