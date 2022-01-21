from __future__ import annotations

from ._abstract import *


class UestcReporter(AbstractReporter):
    """Reporter for UESTC students."""

    def __init__(self, session_id: str) -> None:
        super().__init__('uestc')
        self.set_cookie(SESSION=session_id)

    def run(self) -> str:
        """Run report task.

        Returns:
            Details about report result.
        """
        check_response = self.request('check')
        data: dict = check_response['data']

        # 1. An error occurred during request.
        if data == None:
            raise ReportException(check_response['message'])
        # 2. He has already reported successfully.
        if data['appliedTimes'] != 0:
            return 'reported already'
        # 3. He is away from school.
        if data['schoolStatus'] == 0:
            upload_response = self.request('unreturned')
        # 4. He is at school.
        elif data['schoolStatus'] == 1:
            upload_response = self.request('returned')
        # 5. This branch won't be entered. Just for the sake of caution.
        else:
            raise ReportException('invalid status')

        if upload_response['data'] == True:
            return 'success'
        else:
            return upload_response['message']


def run(info: list[str]) -> str:
    """Simplified API to call from outside the module.

    Returns:
        The result of reporting.
    """
    if len(info) == 0:
        return 'session id not provided'

    session_id, = info
    reporter = UestcReporter(session_id)
    try:
        result = reporter.run()
    except ReportException as e:
        return e
    else:
        return result
