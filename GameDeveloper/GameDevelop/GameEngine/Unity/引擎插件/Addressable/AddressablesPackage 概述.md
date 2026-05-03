
[可寻址资源概述 | Addressables | 1.22.3 --- Addressables overview | Addressables | 1.22.3](https://docs.unity3d.com/Packages/com.unity.addressables@1.22/manual/AddressableAssetsOverview.html)

## Asset addresses  资产地址
您可以根据需要将相同的地址字符串分配给多个资产。例如，如果您拥有某个资产的多个变体，则可以为所有变体分配相同的地址，并使用标签来区分各个变体：

- Asset 1: address: `"plate_armor_rusty"`, label: `"hd"`  
- Asset 2: address: `"plate_armor_rusty"`, label: `"sd"`  

我可以用 MergeMode 和 LoadAssetsAsync 加载两个键的交集

## AssetReference  资产参考

[`AssetReference`](https://docs.unity3d.com/Packages/com.unity.addressables@1.22/api/UnityEngine.AddressableAssets.AssetReference.html) 是一种可以设置为任意 Addressable 资源的类型。Unity 不会自动加载分配给该引用的资源，因此您可以更好地控制何时加载和卸载它。

> 说实话其实不是很理解
> 如何设置？

## Asset loading and unloading  资产加载和卸载


## Dependency and resource managemen 依赖和资源管理

当你加载和释放资源时，Addressables 系统会为每个资源保留一个引用计数。当某个资源不再被引用时，Addressables 会将其卸载。如果该资源所在的 Bundle 中不再包含任何正在使用的资源，Addressables 也会卸载该 Bundle。

## Addressables groups and labels  可寻址组和标签

###   Group schemas  组架构

## Content catalogs  内容目录
由于资产格式是特定于平台的，因此在构建播放器之前必须为每个平台构建内容。

## Play mode scripts  播放模式脚本

## Addressables tools  可寻址工具