import os
import time

from reporter import Reporter

if __name__ == "__main__":
    print(f'[{time.strftime("%F %H:%M:%S")}]', end=' ')

    cookies = os.environ.get('COOKIES')
    if cookies == None:
        raise Exception('session id not provided')
    else:
        cookies = cookies.split('#')

    results = []
    for index, cookie in enumerate(cookies):
        reporter = Reporter(cookie)
        result, message = reporter.run()
        results.append(result)
        print(f'Student {index+1}: {message}')

    if not all(results):
        exit(-1)
