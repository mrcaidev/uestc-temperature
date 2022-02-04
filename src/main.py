import os
import sys
import time

from reporters import UestcReporter

if __name__ == "__main__":
    print(f'[{time.strftime("%F %H:%M:%S")}]', end=' ')
    session_ids = os.environ.get('COOKIES')
    if session_ids == None:
        raise Exception('session id not provided')
    else:
        session_ids = session_ids.split('#')

    for index, session_id in enumerate(session_ids):
        print(f'Student {index+1}:', end=' ')
        reporter = UestcReporter(session_id)
        print(reporter.run())
