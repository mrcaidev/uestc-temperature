import sys
import time

from reporters import *

if __name__ == "__main__":
    print(f'[{time.strftime("%F %H:%M:%S")}]', end=' ')

    # 解析命令行参数，形如 `school#username#password`。
    if len(sys.argv) < 2:
        print('secrets.PASSWORD not provided')
        exit(-1)
    else:
        school, *info = sys.argv[1].split("#")

    # 执行该高校模块的 `run()` 方法。
    try:
        result = eval(f'{school}.run(info)')
    except NameError:
        print(f'module not found: {school}')
    else:
        print(result)
