import json
import os

import requests
from urllib3 import Retry


class Reporter:

    def __init__(self, cookie: str) -> None:
        self.__read_config()
        self.__init_session(cookie)

    def __read_config(self) -> None:
        with open(os.path.join('src', 'config', 'headers.json'), 'r', encoding='utf-8') as fr:
            self.__headers = json.load(fr)
        with open(os.path.join('src', 'config', 'sites.json'), 'r', encoding='utf-8') as fr:
            self.__sites = json.load(fr)

    def __init_session(self, cookie: str) -> None:
        self.__session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=Retry(
            total=50,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        ))
        self.__session.mount('http://', adapter)
        self.__session.mount('https://', adapter)
        self.__session.cookies.update({'SESSION': cookie})

    def __request(self, api: str) -> dict:
        site = self.__sites[api]
        return self.__session.request(
            method=site['method'],
            url=site['url'],
            headers=self.__headers,
            timeout=5,
            json=site['data'],
        ).json()

    def run(self) -> tuple[bool, str]:
        status = self.__request('status')['data']

        if status == None:
            return (False, 'invalid cookie')
        elif status['appliedTimes'] != 0:
            return (True, 'duplicated')
        elif status['schoolStatus'] == 0:
            response = self.__request('unreturned')
        elif status['schoolStatus'] == 1:
            response = self.__request('returned')
        else:
            return (False, 'invalid status')

        if response['data'] == True:
            return (True, 'success')
        else:
            return (False, 'invalid data')
