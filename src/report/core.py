from __future__ import annotations

import json

import requests
import urllib3

from .config import api_dict, common_headers
from .exception import ReportException
from .status import ReportStatus

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Report:
    def __init__(self, session_id: str) -> None:
        self.__headers = common_headers.copy()
        self.__headers["Referer"] += session_id
        self.__headers["Cookie"] += session_id

    def __request(self, api_name: str) -> dict:
        api = api_dict[api_name]
        response = requests.request(
            method=api["method"],
            url=api["url"],
            data=json.dumps(api["data"]),
            headers=self.__headers,
            verify=False,
        )
        return response.json()

    def get_status(self) -> ReportStatus:
        response = self.__request("check")

        data: dict = response.get("data", None)
        if data == None:
            raise ReportException("session id outdated")

        if data["appliedTimes"] != 0:
            raise ReportException("reported already")
        elif data["schoolStatus"] == 0:
            return ReportStatus.unreturned
        elif data["schoolStatus"] == 1:
            return ReportStatus.returned
        else:
            raise ReportException("invalid status")

    def upload(self, status: ReportStatus) -> None:
        response = self.__request(status.name)

        if response["status"] == False:
            raise ReportException("invalid post data")


def run(session_id: str) -> tuple[bool, str]:
    task = Report(session_id)
    try:
        status = task.get_status()
        task.upload(status)
    except ReportException as e:
        return False, e
    else:
        return True, "success"
