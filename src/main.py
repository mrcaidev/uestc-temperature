import json
import os

import requests
from urllib3 import Retry


class Reporter:
    def __init__(self, cookie: str) -> None:
        self.__create_session(cookie)
        self.__read_sites()

    def __read_sites(self) -> None:
        with open(os.path.join("src", "sites.json"), "r", encoding="utf-8") as fr:
            self.__sites = json.load(fr)

    def __create_session(self, cookie: str) -> None:
        self.__session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=Retry(total=50, backoff_factor=0.1)
        )
        self.__session.mount("https://", adapter)
        self.__session.cookies.update({"SESSION": cookie})
        self.__session.headers.update({"content-type": "application/json"})

    def __request(self, api: str) -> dict:
        site: dict = self.__sites[api]
        return self.__session.request(
            method=site["method"],
            url=site["url"],
            timeout=5,
            json=site["data"],
        ).json()

    def run(self) -> tuple[bool, str]:
        status = self.__request("status")["data"]

        if status == None:
            return False, "invalid cookie"
        elif status["appliedTimes"] != 0:
            return True, "duplicated"
        elif status["schoolStatus"] == 0:
            response = self.__request("unreturned")
        elif status["schoolStatus"] == 1:
            response = self.__request("returned")
        else:
            return False, "invalid status"

        if response["status"] == True:
            return True, "success"
        else:
            return False, "invalid data"


if __name__ == "__main__":
    cookies = os.environ.get("COOKIES")
    if cookies == None:
        raise Exception("session id not provided")
    else:
        cookies = cookies.split("#")

    results = []
    for index, cookie in enumerate(cookies):
        reporter = Reporter(cookie)
        result, message = reporter.run()
        results.append(result)
        print(f"Student {index+1}: {message}")

    if not all(results):
        exit(-1)
