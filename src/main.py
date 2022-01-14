import sys

import report

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("session id required")
    else:
        session_ids = sys.argv[1].split("#")

    all_success = True
    for index, session_id in enumerate(session_ids):
        print(f"Reporting for student No.{index+1}:", end=" ")
        success, message = report.run(session_id)
        print(message)
        if not success:
            all_success = False

    if not all_success:
        raise Exception("failed as shown above")
