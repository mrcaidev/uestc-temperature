import sys
import time

from report import ReportTask

if __name__ == '__main__':
    # Parse session IDs.
    if len(sys.argv) != 2:
        raise Exception('Session ID required.')
    else:
        session_ids = sys.argv[1].split('#')

    # Print time for debug purpose.
    print('-' * 60)
    print(time.strftime('%F %H:%M:%S').center(60))
    print(f'{"-"*30}'.center(60))

    # Read configuration files.
    ReportTask.read_config()

    # Run tasks.
    # Async codes not adopted to ensure a higher rate of success.
    for index, session_id in enumerate(session_ids):
        print(f'Reporting for student No.{index+1}:', end=' ')
        task = ReportTask(session_id)
        task.run()
