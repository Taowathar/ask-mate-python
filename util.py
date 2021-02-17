from datetime import datetime
from flask import request


def get_submission_time():
    now = datetime.now().replace(microsecond=0)
    return now


def sorter(query):
    sort_types = {'Title': 'title', 'Submission Time': 'submission_time', 'Message': 'message',
                  'Number of views': 'view_number', 'Number of votes': 'vote_number'}
    directions = {'Ascending': 'ASC', 'Descending': 'DESC'}
    sorting = request.args.get('sorting')
    sorting_direction = request.args.get('sorting_direction')
    if sorting is not None:
        questions = query(sort_types[sorting], directions[sorting_direction])
    else:
        sorting = 'submission_time'
        sorting_direction = 'DESC'
        questions = query(sorting, sorting_direction)
    return questions, sort_types, directions
