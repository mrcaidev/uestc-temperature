import sys
import time

from reporters import *

if __name__ == "__main__":
    print(f'[{time.strftime("%F %H:%M:%S")}]', end=' ')

    # Parse command line arguments.
    if len(sys.argv) < 2:
        raise Exception("user info not provided")
    else:
        school, *info = sys.argv[1].split("#")

    # Execute `run()` defined by this school.
    try:
        result = eval(f'{school}.run(info)')
    except NameError:
        print(f'module not found: {school}')
    else:
        print(result)
