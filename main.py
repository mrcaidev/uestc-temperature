import sys
import time

from reporters import UestcReporter

if __name__ == "__main__":
    print(f'[{time.strftime("%F %H:%M:%S")}]', end=' ')
    session_ids = sys.argv[1].split("#")

    for index, session_id in enumerate(session_ids):
        print(f'Student {index+1}:', end=' ')
        reporter = UestcReporter(session_id)
        print(reporter.run())
