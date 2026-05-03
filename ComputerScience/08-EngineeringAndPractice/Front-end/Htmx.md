
HTMX 的核心思想正是 ​**​"用 HTML 扩展 HTML"​**​，通过简单的 HTML 属性来实现传统上需要编写 JavaScript 的功能，从而大幅简化前端交互开发。

### 典型对比示例
```javascript
// 需要手动编写
document.getElementById('loadBtn').addEventListener('click', async () => {
  const response = await fetch('/api/data');
  const data = await response.text();
  document.getElementById('content').innerHTML = data;
});
```
```html
<!-- 完全用HTML声明实现相同功能 -->
<button id="loadBtn" hx-get="/api/data" hx-target="#content">加载</button>
```