from __future__ import annotations

import json
import os

import requests
from urllib3 import Retry


class AbstractReporter:
    """如果您的上报程序只需要向某些站点 POST 数据即可完成，
    而不涉及模拟浏览器等操作，那么可以考虑继承该抽象类。
    该类可以自动读取配置文件中的 API 与请求头，
    封装了 cookie、request 等操作。
    """

    MAX_RETRIES = 50  # 总共最多重试次数。
    REQ_TIMEOUT = 5  # 单次最长超时时间。

    def __init__(self, school: str) -> None:
        """创建会话，读取配置。"""
        self.__session = self.create_session()
        self.__read_json(school)

    def create_session(self) -> requests.Session:
        """创建新会话。

        Returns:
            自定义过重试规则的新会话。
        """
        session = requests.Session()
        retries = Retry(
            total=self.MAX_RETRIES,  # 自定义最大重试次数。
            backoff_factor=0.1,  # 请求失败后的睡眠时间成倍增加。
            status_forcelist=[500, 502, 503, 504],  # 这些状态码需要强制重试。
        )
        session.mount(
            'http://', requests.adapters.HTTPAdapter(max_retries=retries))
        session.mount(
            'https://', requests.adapters.HTTPAdapter(max_retries=retries))
        return session

    def __read_json(self, school: str) -> None:
        """读取指定高校的配置文件，获取请求头与站点字典。

        Args:
            school: 高校配置文件名，如 "uestc"。
        """
        # 从文件中读取配置字典。
        filepath = os.path.join('config', f'{school}.json')
        try:
            with open(filepath, 'r', encoding='utf-8') as fr:
                conf: dict = json.load(fr)
        except FileNotFoundError:
            print(f'config not found: config/{school}.json')
            exit(-1)

        # 存储至类内。
        self.__session.headers.update(conf.get('headers', {}))
        self.__sites = {site.pop('name'): site for site in conf['sites']}

    def set_cookie(self, **kwargs) -> None:
        """添加 cookie 字段。

        Args:
            **kwargs: 字典形式的 cookie。
        """
        self.__session.cookies.update(kwargs)

    def modify_data(self, api: str, **kwargs) -> None:
        """修改指定 API 的 POST 数据。

        Args:
            api: 要修改数据的 API 名称。
            **kwargs: 字典形式的新 POST 数据。
        """
        if 'data' not in self.__sites[api].keys():
            return
        self.__sites[api]['data'].update(kwargs)

    def request(self, api: str) -> dict:
        """向指定 API 发起请求。

        Args:
            api: 要发起请求的 API 名称。

        Returns:
            JSON 形式的响应。
        """
        site: dict = self.__sites[api]
        response = self.__session.request(
            method=site.get('method', 'get'),
            url=site.get('url', ''),
            timeout=self.REQ_TIMEOUT,
            json=site.get('data', {}),
        )
        return response.json()


class ReportException(Exception):
    """ reporter 域内的自定义异常。"""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.__message = message

    def __repr__(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return self.__message
