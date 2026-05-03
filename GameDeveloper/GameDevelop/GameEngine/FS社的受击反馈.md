【FS社的受击反馈，程序上是怎么做的（上）】 https://www.bilibili.com/video/BV1BAhdz2Ewv/?share_source=copy_web&vd_source=445f9fe806d1b40f2620f76957091c99

## 前置知识
- 动画库
- hks文件触发动画 lua代码
- 状态优先级
	- 6个优先级，决定是否能够覆盖状态
- 冲击力
	- 冲击力编号 从小到大

## ExecDamage

受伤执行顺序判断
