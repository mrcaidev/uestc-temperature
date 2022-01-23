from ._abstract import AbstractReporter


class UestcReporter(AbstractReporter):
    def __init__(self, session_id) -> None:
        super().__init__()
        self.set_cookie(SESSION=session_id)

    def run(self) -> str:
        status = self.request('status')['data']

        if status == None:
            raise Exception('incorrect session id')
        elif status['appliedTimes'] != 0:
            return 'reported already'
        elif status['schoolStatus'] == 0:
            response = self.request('unreturned')
        elif status['schoolStatus'] == 1:
            response = self.request('returned')
        else:
            raise Exception('invalid status')

        if response['data'] == True:
            return 'success'
        else:
            raise Exception('data not acknowledged')
