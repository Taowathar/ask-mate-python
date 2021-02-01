from datetime import datetime


def get_max_id(questions):
    id_list = []
    for question in questions:
        id_list.append(question[0])
    return int(max(id_list)) if len(id_list) != 0 else 0


def get_submission_time():
    now = datetime.now().replace(microsecond=0)
    timestamp = datetime.timestamp(now)
    return int(timestamp)


def from_timestamp_to_time(timestamp):
    return datetime.fromtimestamp(timestamp)
