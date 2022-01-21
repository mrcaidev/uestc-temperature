from __future__ import annotations

import json
import os

import requests
from urllib3 import Retry


class AbstractReporter:

    MAX_RETRIES = 5
    REQ_TIMEOUT = 5

    def __init__(self, school: str) -> None:
        self.__school = school
        self.__sites = self.__read_json('sites')
        self.__headers = self.__read_json('headers')
        self.__cookies = {}
        self.__create_session()

    def __read_json(self, filename: str) -> dict:
        """Read config json under config directory.

        Args:
            The filename of config without extension.
        """
        filepath = os.path.join('config', self.__school, f'{filename}.json')
        try:
            with open(filepath, 'r', encoding='utf-8') as fr:
                return json.load(fr)
        except FileNotFoundError:
            return {}

    def __create_session(self) -> None:
        """Create a session for the student."""
        self.__session = requests.Session()
        retries = Retry(
            total=self.MAX_RETRIES,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        self.__session.mount(
            'http://', requests.adapters.HTTPAdapter(max_retries=retries))
        self.__session.mount(
            'https://', requests.adapters.HTTPAdapter(max_retries=retries))

    def set_cookie(self, **kwargs) -> None:
        """Set the cookie to identify the student.

        Args:
            **kwargs: Cookie items.
        """
        self.__cookies.update(kwargs)

    def modify_data(self, api: str, **kwargs) -> None:
        """Modify data of specified api.

        Args:
            api: The name of API whose data will be modified.
            **kwargs: New data set.
        """
        if 'data' not in self.__sites[api].keys():
            return
        self.__sites[api]['data'].update(kwargs)

    def request(self, api: str) -> dict:
        """Issue request towards the specified api.

        Args:
            api: The name of API recorded in config file.
        """
        site: dict = self.__sites[api]
        response = self.__session.request(
            method=site.get('method', 'get'),
            url=site.get('url', ''),
            headers=self.__headers,
            cookies=self.__cookies,
            timeout=self.REQ_TIMEOUT,
            json=site.get('data', {}),
        )
        return response.json()


class ReportException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.__message = message

    def __repr__(self) -> str:
        return self.__message

    def __str__(self) -> str:
        return self.__message
