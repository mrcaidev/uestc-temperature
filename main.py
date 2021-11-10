import random
import sys
import time

import requests
import urllib3


class Report:
    def __init__(self) -> None:
        if (len(sys.argv) != 2):
            print('Cookie is needed!')
            exit(-1)
        self.cookies = sys.argv[1].split("#")
        self.headers = {
            "content-type": "application/json",
            "connection": "close"
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
            "todayMorningTemperature": "36.5°C~36.9°C",
            "yesterdayEveningTemperature": "36.5°C~36.9°C",
            "yesterdayMiddayTemperature": "36.5°C~36.9°C",
            "location": "四川省成都市郫都区丹桂路",
            "healthColor": "绿色"
        }
        # 记录上报结果。
        self.success = 0
        self.done = 0
        self.fail = 0

    def check_student_status(self) -> int:
        """检查学生的当前状态。
        ---
        当前状态包括<上报状态>与<在校状态>，据此返回不同的状态码，决定当前循环要采取的行动。

        :return: `int` 学生当前的状态码。
        - 0 : 发生错误
        - 1 : 已经上报
        - 2 : 未上报，不在校
        - 3 : 未上报，在校
        """
        try:
            response = requests.get(
                url="https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/checkRegisterNew",
                headers=self.headers,
                verify=False
            )
        except Exception as e:
            self.fail += 1
            print(e)
            return 0
        if response.status_code != 200:
            self.fail += 1
            print("Failed: Network trouble.")
            return 0

        data: dict = response.json()["data"]
        if data == None:
            self.fail += 1
            print("Failed: Wrong cookie.")
            return 0

        reported_times: int = data.get("appliedTimes", None)
        if reported_times == None:
            self.fail += 1
            print("Failed: appliedTimes == None.")
            return 0
        elif reported_times != 0:
            self.done += 1
            print("Already reported.")
            return 1
        else:
            is_at_school: int = data.get("schoolStatus", None)
            if is_at_school == None:
                self.fail += 1
                print("Failed: schoolStatus == None.")
                return 0
            elif is_at_school == 0:
                return 2
            elif is_at_school == 1:
                return 3
            else:
                self.fail += 1
                print("Failed: Invalid school status.")
                return 0

    def report_data(self, url, data) -> None:
        """进行上报。
        ---
        根据学生状态选择对应的数据，上传到对应的站点。

        :param url: 站点，在校和不在校两种状态，对应的上报站点不同。
        :param data: 数据，包括体温、地点等。
        """
        try:
            response = requests.post(
                url=url,
                headers=self.headers,
                data=str(data).encode("utf-8"),
                verify=False
            )
        except Exception as e:
            self.fail += 1
            print(e)
            return
        if response.status_code != 200:
            self.fail += 1
            print("Failed: Network trouble.")
            return

        is_success: bool = response.json().get("status", None)
        if is_success == None:
            self.fail += 1
            print("Failed: status == None.")
        elif is_success == False:
            self.fail += 1
            print("Failed: Invalid post data.")
        else:
            self.success += 1
            print("Success.")

    def run(self):
        for index, cookie in enumerate(self.cookies):
            print(f"Reporting for student No.{index+1}...", end="")
            self.headers.update({"cookie": cookie})

            student_status = self.check_student_status()
            if student_status == 2:
                self.report_data(url=self.unreturned_url,
                                 data=self.unreturned_data)
            elif student_status == 3:
                self.report_data(url=self.returned_url,
                                 data=self.returned_data)
            else:
                continue


if __name__ == "__main__":
    time.sleep(random.randint(0, 10))

    print("-" * 60)
    print(time.strftime("%F %H:%M:%S").center(60))
    print("------------".center(60))

    app = Report()
    app.run()

    print(
        f"Finished: {app.success} success, {app.done} done, {app.fail} failed."
    )
