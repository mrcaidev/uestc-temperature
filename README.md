# UESTC_Temperature

---

> 关于我，欢迎关注：
>
> Github 主页：[MrCaiDev](https://github.com/MrCaiDev)
>
> 个人邮箱：1014305148@qq.com
>
> 工作邮箱：yuwangcai@std.uestc.edu.cn

---

## 项目介绍

电子科技大学（UESTC）每日体温自动填报。

- **本项目仅适用于：微信小程序 ->  “uestc学生情况报送”！**
- 工作流将自动在每日的**00:30**发起上报，全过程无需用户执行任何操作。
- 本项目的思路有参考[checkmate1816/uestc_temperature_report](https://github.com/checkmate1816/uestc_temperature_report)，但使用了Python进行重构。
- 对代码改进有任何好的建议，欢迎提`Issues`，或者直接`PR`！我期待看到不同的想法！
- 如果对您有帮助，请顺手点个`Star`吧~

---

## 使用方法

1. 开始之前，你需要先下载这两个软件（教程结束后可以卸载）：

     - [微信电脑版](https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe)
     - [Fiddler Classic](https://telerik-fiddler.s3.amazonaws.com/fiddler/FiddlerSetup.exe)
2. 抓包获取Cookie。

     1. 打开Fiddler，点击`Tools`下的`Options`，对照下面三张图检查配置。

          ![General栏](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/1.png)

          ![HTTPS栏](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/2.png)

          ![Connections栏](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/3.png)

     2. 为Fiddler安装证书，如下面的流程所示。

          ![入口](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/4.png)

          ![提示](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/5.png)

          ![确认](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/6.png)

          ![成功](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/7.png)

     3. 确认证书成功安装后，重启Fiddler。

          ![入口](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/8.png)

          ![检测](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/9.png)

     4. 打开微信小程序“uestc学生情况报送”。

          ![小程序](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/10.png)

     5. 在Fiddler中找到这个数据包，里面存放着你的Cookie。

          ![数据包](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/11.png)

3. 将Cookie添加到仓库。

     1. 将本仓库`Fork`到自己的仓库中。

          ![Fork](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/14.png)

     2. 点击`Settings`→`Secrets`→`New repository secret`。

          ![secrets](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/12.png)

     3. 在`Name`中填入`COOKIES`，在`Value`中填入刚刚记录的Cookie；如果有多个人的Cookie，就用`#`隔开。最后点击`Add Secret`。

          ![填入信息](https://raw.githubusercontent.com/MrCaiDev/uestc_temperature/master/tutorial_images/13.png)

4. 至此配置全部完成，你可以在第二天检查是否成功填报；如果没有，请通过`Issues`联系我。微信电脑版和Fiddler现在可以卸载。

---

## TODO

1. 完善当前不在校的自动填报数据。

---

## 注意事项

本项目仅供学习参考之用，如果因为本项目导致意外情况的发生（几率极小），本项目及其作者不承担相应责任。
