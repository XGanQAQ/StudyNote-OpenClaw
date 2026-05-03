
## 分享一个避免浏览器开[http://unity.com](https://link.zhihu.com/?target=http%3A//unity.com)会自动跳转到[http://unity.cn](https://link.zhihu.com/?target=http%3A//unity.cn)的方法

需要准备一个国外的梯子，然后按以下步骤操作：

1. 开[全局代理](https://zhida.zhihu.com/search?content_id=715727440&content_type=Answer&match_order=1&q=%E5%85%A8%E5%B1%80%E4%BB%A3%E7%90%86&zhida_source=entity)（或者用[通配符](https://zhida.zhihu.com/search?content_id=715727440&content_type=Answer&match_order=1&q=%E9%80%9A%E9%85%8D%E7%AC%A6&zhida_source=entity) `*.unity.*`给unity单独设置代理也行）
2. 关闭浏览器的所有unity相关页面
3. 在浏览器设置中，搜索 unity 相关的[cookie](https://zhida.zhihu.com/search?content_id=715727440&content_type=Answer&match_order=1&q=cookie&zhida_source=entity)，把搜索结果列出来的项目全都删除

![](https://pic1.zhimg.com/80/v2-bb2ad3c8f1c57d7a9b11ffc33745d1aa_1440w.webp?source=1def8aca)

删除Unity相关Cookie

4. 在浏览器设置中，阻止 [unity.cn](https://link.zhihu.com/?target=http%3A//unity.cn/) 保存cookie，填写 `[*.]unity.cn`

![](https://pic1.zhimg.com/80/v2-158519a96fdd0df370e81ac97397d560_1440w.webp?source=1def8aca)

阻止unity.cn保存Cookie

5. 重启浏览器

之后访问 [unity.com](https://link.zhihu.com/?target=http%3A//unity.com/) 时就不会再自动跳转到 cn 了（代理不能关），不过还是会跳转到 [unity.com/cn](https://link.zhihu.com/?target=http%3A//unity.com/cn/) ，但内容依然是国际版，可以正常看到unity 6，也可以手动删除 /cn

![](https://picx.zhimg.com/80/v2-892825abdc9a5dbaad3cb903a3f5342d_1440w.webp?source=1def8aca)

## 登录到国际版账户问题

哪怕你挂了代理点击login，仍然是登录的.cn的网址。我们只需要先按照上面的要求，清理cookie,再挂上全局代理，在点击登录的时候，把api.unity.cn 改成 api.unity.com 就行了