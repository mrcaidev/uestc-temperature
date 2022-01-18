# uestc-temperature

## 项目介绍

电子科技大学本科生每日体温自动填报。

- 本项目仅适用于微信小程序**智慧学工 -> 疫情防控**；
- 工作流将在每日的 **00:30** 左右自动上报，略有几分钟延迟为正常状况，配置完成后无需用户执行任何操作。
- 支持托管多人自动上报，见[部署方法](https://github.com/MrCaiDev/uestc-temperature#部署方法)。
- 支持在校和离校学生的填报。
- 如果对您有帮助，请顺手点个 ⭐Star⭐ 吧！

## 部署方法

### GitHub 自动化部署（推荐）

#### 第一步：抓取 Cookie

从“成电智慧学工”公众号的“体温测量通知”进入上报页面，在右上角的“...”中点击复制链接，可以得到如下字样：

    https://jzsz.uestc.edu.cn/epidemic2/sessionId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx#/pages/epidemic/everyDay/everyDay

复制其中的 `sessionId` 字段，即 `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` 字样。这就是稍后需要用到的 Cookie。

#### 第二步：部署 Action

- 点击[本页面](https://github.com/MrCaiDev/uestc-temperature)右上角的 Fork，将本仓库复制到自己名下；
- 在自己的仓库内，点击 Settings -> Secrets -> New repository secret；
- 在 Name 中填入 COOKIES ，在 Value 中填入[第一步](https://github.com/MrCaiDev/uestc-temperature#第一步：抓取%20Cookie)中抓取的 Cookie；如果有多个人的 Cookie，就用 `#` 隔开。最后点击 Add Secret；
- 完成后，进入仓库的 Actions 界面。仓库的工作流默认不开启，请手动打开（只要手动打开一次就行）。您也可以手动执行 Daily Report -> Run workflow -> Run workflow，以检验工作是否正常。

### 本地私有部署

> 需要本地拥有 Python 环境，最低兼容版本为 3.9；若您的 Python 版本在 3.6-3.8 间，请手动清除类型注释，或在具有类型注释的 Python 文件开头添加 `from __future__ import annotations`。
> 
> 本项目仅在 Ubuntu-20.04 上得到测试，若 windows 下无法运行，请在 Issue 中提供具体信息。
> 
> 本项目不提供本地的自动化支持，需要部署者自行解决每日自动化问题。（如 PowerAutomate 等自动化软件）

- 将仓库克隆到本地：`git clone https://github.com/MrCaiDev/uestc-temperature.git`
- 进入项目根目录：`cd uestc-temperature`
- 下载项目依赖：`pip install -r requirements.txt`
- 执行脚本：`python -u src/main.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## 注意事项

- 本项目仅供学习参考之用，如果因为本项目导致意外情况的发生（几率极小），本项目及其作者不承担相应责任。
- Session ID 会过期，保质期从 3 天到 15 天不等；目前仍未找到好的解决方案，恳请有兴趣的朋友共同探讨！
