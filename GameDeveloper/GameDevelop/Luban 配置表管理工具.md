[Luban | Luban](https://luban.doc.code-philosophy.com/)

**Luban的作用**
Luban 在我看来，是打通了从Excel族到json等格式数据之间的通路，并支持生成对应语言代码的功能

**放下Assets报错**
Luban的dll文件如果直接放在Assets文件夹下会报错（虽然说可以正常运行）（网上教程说打开unsafe模式不会要报错，但是我照做还是不行），由于只需要它作为转换Excel 到 Json 和生成代码的工具，放在Assets外也无所谓。

**Luban配置文件**
luban.conf中可以配置存放表格的目录（正常为Datas，可以不做调整）

**添加新表格**
在Datas中创建一个表格，安装其格式规范输入数据
然后再_tables_中添加相关配置，即可让新建的表格加入

**支持自定义类型**
[使用自定义类型 | Luban](https://www.datable.cn/docs/beginner/usecustomtype)

**使用方法**
只要配置好命令行/Bat脚本中的路径，gen就会自动安装其路径生成正确的Json和代码文件
所以我编写了一个Unity编辑器窗口工具，在编辑器界面运行bat脚本

## 运行时读取配置
需要让Unity用PackageManager URL 安装一个包，用来运行时读取配置
[focus-creative-games/luban_unity: unity package for luban](https://github.com/focus-creative-games/luban_unity)

```cs
//加载配置
string gameConfDir = "<outputDataDir>"; // 替换为gen.bat中outputDataDir指向的目录
var tables = new cfg.Tables(file => JSON.Parse(File.ReadAllText($"{gameConfDir}/{file}.json")));

//使用配置
cfg.demo.Reward reward = tables.TbReward.Get(1001);
Console.WriteLine("reward:{0}", reward);


// 示例2 
void Load()  
{  
// 一行代码可以加载所有配置。 cfg.Tables 包含所有表的一个实例字段。  
var tables = new cfg.Tables(Loader);  
// 访问一个单例表  
Console.WriteLine(tables.TbGlobal.Name);  
// 访问普通的 key-value 表  
Console.WriteLine(tables.TbItem.Get(12).Name);  
// 支持 operator []用法  
Console.WriteLine(tables.TbMail[1001].Desc);  
}  
  
private static JSONNode LoadJson(string file)  
{  
return JSON.Parse(File.ReadAllText($"{your_json_dir}/{file}.json", System.Text.Encoding.UTF8));  
}
```