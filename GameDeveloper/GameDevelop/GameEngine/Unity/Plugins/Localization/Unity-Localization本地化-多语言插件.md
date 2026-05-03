## 支持功能

- 多语言映射
	- 静态文本
	- 动态文本
	- 资源多语言映射
- 导入导出CSV

## 教程参考

[【Unity 实用工具篇】| 游戏多语言解决方案，官方插件Localization 实现本地化及多种语言切换-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2370376)

[Quick Start Guide | Localization | 1.5.4](https://docs.unity3d.com/Packages/com.unity.localization@1.5/manual/QuickStartGuideWithVariants.html)

## 注意事项

- CSV表格修改要改成`UTF-8的编码格式`再保存文件，不然导入之后中文会显示乱码。
- 打包项目的话还需要对Localization Tables进行Build

