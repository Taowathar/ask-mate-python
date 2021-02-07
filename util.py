from datetime import datetime


def get_max_id(questions):
    id_list = []
    for question in questions:
        id_list.append(question['id'])
    return int(max(id_list)) if len(id_list) != 0 else 0


def get_submission_time():
    now = datetime.now().replace(microsecond=0)
    timestamp = datetime.timestamp(now)
    return int(timestamp)


def from_timestamp_to_time(timestamp):
    return datetime.fromtimestamp(timestamp)


def sorter(sorting, sorting_direction, data):
    check_list = ["Title", "Message"]
    if sorting in check_list:
        if sorting == "Title":
            sort_id = 'title'
        elif sorting == "Message":
            sort_id = 'message'
        new_data = []
        while data:
            minimum = data[0][sort_id]
            minimum_row = data[0]
            for row in data:
                if row[sort_id] < minimum:
                    minimum = row[sort_id]
                    minimum_row = row
            new_data.append(minimum_row)
            data.remove(minimum_row)
        if sorting_direction == "Ascending":
            return new_data
        else:
            return list(reversed(new_data))
    else:
        if sorting == "Submission Time":
            sort_id = 'id'
        elif sorting == "Number of views":
            sort_id = 'view_number'
        elif sorting == "Number of votes":
            sort_id = 'vote_number'
        new_data = []
        while data:
            minimum = int(data[0][sort_id])
            minimum_row = data[0]
            for row in data:
                if int(row[sort_id]) < minimum:
                    minimum = int(row[sort_id])
                    minimum_row = row
            new_data.append(minimum_row)
            data.remove(minimum_row)
        if sorting_direction == "Ascending":
            return new_data
        else:
            return list(reversed(new_data))
