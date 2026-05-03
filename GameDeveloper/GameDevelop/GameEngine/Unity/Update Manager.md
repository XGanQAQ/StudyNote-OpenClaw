[【Unity】使用Update管理器优化性能_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1dKxezqEpU/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=1015af2504b4c9c5deda584505666669)

Update函数在调用前会进行一系列的条件检测，但存在大量Update的时候，这会造成不必要的性能开销。
使用Update Manager 实现观察者模式，从而为所有对象统一Update的入口，实现统一的Update。从而避免了这些开销。