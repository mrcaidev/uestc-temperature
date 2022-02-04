import json

import requests
from urllib3 import Retry


class AbstractReporter:
    def __init__(self) -> None:
        self.__create_session()
        self.__read_json()

    def __create_session(self) -> None:
        self.__session = requests.Session()
        retries = Retry(
            total=50,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
        self.__session.mount(
            'http://', requests.adapters.HTTPAdapter(max_retries=retries))
        self.__session.mount(
            'https://', requests.adapters.HTTPAdapter(max_retries=retries))

    def __read_json(self) -> None:
        with open('src/config/headers.json', 'r', encoding='utf-8') as fr:
            self.__session.headers.update(json.load(fr))
        with open('src/config/sites.json', 'r', encoding='utf-8') as fr:
            self.__sites = json.load(fr)

    def set_cookie(self, **kwargs) -> None:
        self.__session.cookies.update(kwargs)

    def request(self, api) -> dict:
        site = self.__sites[api]
        response = self.__session.request(
            method=site['method'],
            url=site['url'],
            timeout=5,
            json=site['data'],
        )
        return response.json()
