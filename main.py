import random
import sys
import time

import requests


class Report:
    """自动完成体温上报。"""

    def __init__(self) -> None:
        """设定固定的参数。"""

        # 读取命令行的 Cookies。（存放在仓库的`Secrets`中）
        self.cookies = sys.argv[1].split("#")

        # 请求头，后续会加入 cookie。
        self.headers = {"content-type": "application/json", "Connection": "close"}

        # 未返校学生的站点和数据。
        self.unreturned_url = ""  # TODO Not verified yet.
        self.unreturned_data = {
            # TODO Not verified yet.
        }

        # 返校学生的站点和数据。
        self.returned_url = (
            "https://jzsz.uestc.edu.cn/wxvacation/monitorRegisterForReturned"
        )
        self.returned_data = {
            "healthCondition": "正常",
            "todayMorningTemperature": "36°C~36.5°C",
            "yesterdayEveningTemperature": "36°C~36.5°C",
            "yesterdayMiddayTemperature": "36°C~36.5°C",
            "location": "四川省成都市郫都区银杏大道",
        }

        # 记录上报结果。
        self.success = 0
        self.done = 0
        self.fail = 0

    def check_status(self) -> int:
        """检查学生的当前状态。
        ---
        当前状态包括<上报状态>与<在校状态>，据此返回不同的状态码，决定当前循环要采取的行动。

        :return: `int` 学生当前的状态码。
        - 0 : 发生错误
        - 1 : 已经上报
        - 2 : 未上报，不在校
        - 3 : 未上报，在校
        """
        # 尝试对查询站点发起请求。
        try:
            response = requests.get(
                "https://jzsz.uestc.edu.cn/wxvacation/checkRegisterNew",
                headers=self.headers,
                verify=False,
            )
        except Exception as e:
            self.fail += 1
            print(e)
            return 0

        # 如果状态码不为 200：
        if response.status_code != 200:
            self.fail += 1
            print("Failed: Network trouble.")
            return 0

        # 解析查询到的字典。
        data: dict = response.json()["data"]
        if data == None:
            self.fail += 1
            print(
                "Failed: Cookie should be like: JSESSIONID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            return 0

        # 检查上报次数。
        applied_times: int = data.get("appliedTimes", None)
        # 如果找不到该字段：
        if applied_times == None:
            self.fail += 1
            print("Failed: Not your problem.")
            return 0
        # 如果已经上报过了：
        elif applied_times != 0:
            self.done += 1
            print("Already reported.")
            return 1
        # 如果还没上报：
        else:
            # 检查在校状态。
            school_status: int = data.get("schoolStatus", None)
            # 如果找不到该字段：
            if school_status == None:
                self.fail += 1
                print("Failed: Not your problem.")
                return 0
            # 如果不在校：
            elif school_status == 0:
                return 2
            # 如果在校：
            elif school_status == 1:
                return 3
            # 如果出现其他未知的数字：
            else:
                self.fail += 1
                print("Failed: Invalid school status.")
                return 0

    def do_report(self, url, data) -> None:
        """进行上报。
        ---
        根据学生状态选择对应的数据，上传到对应的站点。

        :param url: 站点，在校和不在校两种状态，对应的上报站点不同，
        :param data: 数据，包括体温、地点等。
        """
        # 尝试对上报站点发起请求。
        try:
            response = requests.post(
                url, headers=self.headers, data=str(data).encode("utf-8"), verify=False
            )
        except Exception as e:
            self.fail += 1
            print(e)
            return

        # 如果状态码不为 200：
        if response.status_code != 200:
            self.fail += 1
            print("Failed: Network trouble.")
            return

        # 解析返回的状态字典。
        report_status: bool = response.json().get("status", None)
        # 如果找不到该字段：
        if report_status == None:
            self.fail += 1
            print("Failed: Not your problem.")
        # 如果上报失败：
        elif report_status == False:
            self.fail += 1
            print("Failed: Data posted, but report failed.")
        # 如果上报成功：
        else:
            self.success += 1
            print("Success.")

    def run(self):
        # 遍历每位学生。
        for index, cookie in enumerate(self.cookies):
            print(f"Reporting for student No.{index+1}...", end="")
            # 为这位同学定制请求头。
            self.headers.update({"cookie": cookie})
            status = self.check_status()
            # 如果未上报且不在校：
            if status == 2:
                self.do_report(url=self.unreturned_url, data=self.unreturned_data)
            # 如果未上报且在校：
            elif status == 3:
                self.do_report(url=self.returned_url, data=self.returned_data)
            # 如果出错或已经上报：
            else:
                continue


if __name__ == "__main__":
    # 睡眠随机时间。
    time.sleep(random.randint(0, 10))
    # 提示开始。
    start = time.time()
    print("-" * 60)
    print(time.strftime("%F %H:%M:%S").center(60))
    print("------------".center(60))

    # 运行程序。
    app = Report()
    app.run()

    # 提示结束。
    end = time.time()
    print("-" * 60)
    print(
        f"Finished in {round(end-start, 2)} seconds: {app.success} success, {app.done} done, {app.fail} failed."
    )
