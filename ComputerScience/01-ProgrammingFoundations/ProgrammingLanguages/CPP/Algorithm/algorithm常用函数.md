在 C++ 算法程序设计中，有一些常用的函数和标准库算法可以帮助你高效地解决问题。以下是一些常用的函数和算法：
```cpp
#include <algorithm>
```
1. **排序相关**：
   - `std::sort(begin, end)`：对范围内的元素进行排序。
   ```cpp
    std::vector<int> vec = {5, 2, 9, 1, 5, 6};
    std::sort(vec.begin(), vec.end()); //升序
    std::sort(vec.begin(), vec.end(), std::greater<int>());//降序
   ```

   - `std::stable_sort(begin, end)`：稳定排序，保持相等元素的相对顺序。

2. **查找相关**：
   - `std::find(begin, end, value)`：查找容器中第一个等于 `value` 的元素。
   - `std::binary_search(begin, end, value)`：在已排序的范围内查找 `value` 是否存在。
   - `std::lower_bound(begin, end, value)`：返回第一个不小于 `value` 的元素位置。
   - `std::upper_bound(begin, end, value)`：返回第一个大于 `value` 的元素位置。

3. **集合相关**：
   - `std::set_intersection(begin1, end1, begin2, end2, output)`：计算两个集合的交集。
   - `std::set_union(begin1, end1, begin2, end2, output)`：计算两个集合的并集。
   - `std::set_difference(begin1, end1, begin2, end2, output)`：计算两个集合的差集。

4. **变换相关**：
   - `std::transform(begin, end, output, func)`：对范围内的元素应用函数 `func` 并输出到 `output`。
   - `std::reverse(begin, end)`：反转范围内的元素。

5. **统计相关**：
   - `std::count(begin, end, value)`：计算等于 `value` 的元素个数。
   - `std::accumulate(begin, end, initial)`：计算范围内所有元素的和。

6. **随机数相关**：
   - `std::shuffle(begin, end, rng)`：随机打乱范围内的元素。
   - `std::rand()` 和 `std::srand(seed)`：生成随机数。

这些函数和算法大多定义在 `<algorithm>` 头文件中。使用它们可以大大简化代码，提高程序的效率。你有特定的算法或数据结构想要深入了解吗？