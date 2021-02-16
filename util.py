from datetime import datetime


def get_submission_time():
    now = datetime.now().replace(microsecond=0)
    return now


