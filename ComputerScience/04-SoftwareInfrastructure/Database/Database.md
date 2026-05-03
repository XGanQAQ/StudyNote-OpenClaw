# 数据库

## 基本概念

### 关系型数据库
- **表 (Table)**：行+列的结构化数据存储
- **行 (Row/Tuple)**：一条记录
- **列 (Column/Attribute)**：一个字段
- **主键 (Primary Key)**：唯一标识一行
- **外键 (Foreign Key)**：引用其他表的主键
- **索引 (Index)**：加快查找速度

### 范式 (Normalization)
| 范式 | 要求 |
|------|------|
| 1NF | 列不可再分（原子性） |
| 2NF | 非主属性完全函数依赖于候选键 |
| 3NF | 非主属性不传递依赖于候选键 |
| BCNF | 所有函数依赖的决定因素都是候选键 |

### 完整性约束
- 实体完整性：主键不为空
- 参照完整性：外键必须引用存在的行
- 用户定义完整性：CHECK 约束等

## SQL 语句速查

### 数据查询
```sql
SELECT column1, column2 FROM table WHERE condition
ORDER BY column ASC/DESC
GROUP BY column HAVING condition
LIMIT n OFFSET offset
```

### 数据操作
```sql
INSERT INTO table VALUES (...)
UPDATE table SET column=value WHERE condition
DELETE FROM table WHERE condition
```

### 表操作
```sql
CREATE TABLE table (...)
ALTER TABLE table ADD column type
DROP TABLE table
```

### SQL 函数
- 文本函数：CONCAT, SUBSTRING, LENGTH, UPPER
- 数值函数：ROUND, ABS, CEILING, FLOOR
- 聚合函数：COUNT, SUM, AVG, MAX, MIN
- 日期函数：YEAR, MONTH, DAY, DATE_FORMAT

### 高级查询
- JOIN：INNER/LEFT/RIGHT/FULL
- 子查询：WHERE IN (SELECT ...)
- UNION：合并结果集
- 窗口函数：ROW_NUMBER, RANK, DENSE_RANK

## 数据库应用

### ORM (对象关系映射)
- 将数据库表映射为编程语言的对象
- 代表：Entity Framework, SQLAlchemy, Prisma
- 优点：减少重复 SQL，面向对象操作
- 缺点：性能开销，复杂查询仍需手写

### 常用数据库
| 数据库 | 特点 | 适用场景 |
|--------|------|---------|
| MySQL | 流行、社区支持好 | Web 应用 |
| PostgreSQL | 功能强大、扩展性好 | 复杂应用 |
| SQLite | 嵌入式、零配置 | 本地/移动应用 |
| SQL Server | 微软生态 | 企业应用 |

## SQL Server 特性
- [触发器](SQL-Server/触发器.md)：自动执行的操作
- [视图](SQL-Server/视图.md)：虚拟表
- [权限控制](SQL-Server/权限控制.md)：用户权限管理
- [多表查询](SQL-Server/多表查询.md)
- [空值处理](SQL-Server/空值处理.md)
