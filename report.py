import os
from json import load

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Status:
    """Current status code of a student."""
    reported = 1
    returned = 2
    unreturned = 3


class ReportError(Exception):
    """Exceptions that may occur during report process."""
    pass


class ReportTask:
    """Temperature report task for a single student."""

    def __init__(self, session_id: str) -> None:
        """Init report task.

        Args:
            session_id: The session ID representing the student.
        """
        self.headers = ReportTask.headers.copy()
        self.headers.update({
            'Referer': f'{ReportTask.referer}{session_id}',
            'Cookie': f'SESSION={session_id}'
        })

    @classmethod
    def read_config(cls) -> None:
        """Read headers and API from JSON config.

        Note:
            Headers in JSON file does not contain any specified data.
        """
        # Read headers.
        with open(os.path.join('config', 'headers.json'), 'r', encoding='utf-8') as fr:
            cls.headers: dict = load(fr)

        # Read API.
        with open(os.path.join('config', 'api.json'), 'r', encoding='utf-8') as fr:
            api_dict: dict = load(fr)

        # Parse API.
        cls.check_url: str = api_dict['checkUrl']
        cls.referer: str = api_dict['referer']
        cls.returned_url: str = api_dict['returnedUrl']
        cls.returned_data: dict = api_dict['returnedData']
        cls.unreturned_url: str = api_dict['unreturnedUrl']
        cls.unreturned_data: dict = api_dict['unreturnedData']

    def _check_status(self) -> Status:
        """Check the current status of the student.

        The status includes:
            - Whether he has reported.
            - Whether he has returned to school.

        Returns:
            Code indicating the current status of the student.
        """
        # Request checking API.
        response = requests.get(
            url=self.check_url,
            headers=self.headers,
            verify=False,
        )
        if response.status_code != 200:
            raise ReportError('Network trouble.')
        response_json: dict = response.json()

        # Parse data.
        data: dict = response_json.get('data', None)
        if not data:
            raise ReportError('Session ID outdated.')

        # Check report status.
        reported_times: int = data.get('appliedTimes', None)
        if reported_times == None:
            raise ReportError('appliedTimes == None.')
        elif reported_times != 0:
            print('Already reported.')
            return Status.reported

        # Check school status.
        school_status: int = data.get('schoolStatus', None)
        if school_status == None:
            raise ReportError('schoolStatus == None.')
        elif school_status == 0:
            return Status.unreturned
        elif school_status == 1:
            return Status.returned
        else:
            raise ReportError('Invalid school status.')

    def _upload_data(self, status_code: Status) -> None:
        """Upload appropriate temperature data to school API.

        Args:
            status_code: The status code of the student.
        """
        # Request uploading API.
        if status_code == Status.returned:
            response = requests.post(
                url=ReportTask.returned_url,
                headers=self.headers,
                data=str(ReportTask.returned_data).encode('utf-8'),
                verify=False
            )
        else:
            response = requests.post(
                url=ReportTask.unreturned_url,
                headers=self.headers,
                data=str(ReportTask.unreturned_data).encode('utf-8'),
                verify=False
            )
        if response.status_code != 200:
            raise ReportError('Network trouble.')
        response_json: dict = response.json()

        # Check report status.
        report_status: bool = response_json.get('status', None)
        if report_status == None:
            raise ReportError('status == None.')
        elif report_status == False:
            raise ReportError('Invalid post data.')
        else:
            print('Success.')

    def run(self) -> bool:
        """Run report task.

        Returns:
            `True` on success, or `False` on failure.
        """
        try:
            status = self._check_status()
            if status != Status.reported:
                self._upload_data(status)
        except ReportError as e:
            print(e)
            return False
        else:
            return True
