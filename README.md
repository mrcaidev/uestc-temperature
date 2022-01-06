# uestc-temperature

> 关于我，欢迎关注：
>
> 个人博客：[mrcai.space](https://mrcai.space)
>
> Github 主页：[MrCaiDev](https://github.com/MrCaiDev)
>
> 个人邮箱：[1014305148@qq.com](mailto:1014305148@qq.com)
>
> 工作邮箱：[yuwangcai@std.uestc.edu.cn](mailto:yuwangcai@std.uestc.edu.cn)

## 项目介绍

电子科技大学（UESTC）每日体温自动填报。

- 本项目仅适用于微信小程序**智慧学工→疫情防控**；
- 工作流将自动在每日的**01:30**发起上报，略有几分钟延迟为正常状况，全过程无需用户执行任何操作。
- 对代码改进有任何好的建议，欢迎提`Issues`，或者直接`PR`！
- 如果对您有帮助，请顺手点个⭐`Star`⭐吧~

## 使用方法

1. 抓取cookie。

进入您微信中的“每日填报”界面，在右上“...”中复制链接，可以得到如下字样：

    https://jzsz.uestc.edu.cn/epidemic2/sessionId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx#/pages/epidemic/everyDay/everyDay

复制其中的 `sessionId`，即 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 字段。这就是需要用到的 Cookie。


2. 部署Action。

   1. 将本仓库`Fork`到自己的仓库里；

   ![1](https://raw.githubusercontent.com/MrCaiDev/uestc-temperature/master/images/1.png)

   1. 点击`Settings`→`Secrets`→`New repository secret`。

   ![2](https://raw.githubusercontent.com/MrCaiDev/uestc-temperature/master/images/2.png)

   1. 在`Name`中填入`COOKIES`，在`Value`中填入刚刚记录的cookie；如果有多个人的cookie，就用`#`隔开。最后点击`Add Secret`。

   ![3](https://raw.githubusercontent.com/MrCaiDev/uestc-temperature/master/images/3.png)

   1. 完成后，进入`Actions`界面。被`Fork`仓库的工作流默认不开启，请手动打开（只要手动打开一次就行）。你也可以手动执行工作流，检验程序能否执行。

   ![4](images/2021-11-10-17-00-54.png)

## TODO

1. 支持当前不在校学生的填报。
2. 支持研究生网上平台的填报。

## 注意事项

- 本项目仅供学习参考之用，如果因为本项目导致意外情况的发生（几率极小），本项目及其作者不承担相应责任。
- 目前发现Cookie可能会过期，保质期未知！
