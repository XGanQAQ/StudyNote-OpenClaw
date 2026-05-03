理解 **SO 从磁盘到内存的完整流程**
# ScriptableObject 的存储与生命周期

## 存储位置
Assets/xxx/Config.asset

## 初始化流程
1. Unity 发现 Asset
2. 反序列化 .asset 文件
3. 在内存中生成对象实例
4. 所有引用指向同一个实例

## 重要结论
ScriptableObject 是「资产级单例」
