# import csv
# import os
# from werkzeug.utils import secure_filename
# from flask import request


import connection
from psycopg2.extras import RealDictCursor


# QUESTIONS = 'sample_data/question.csv'
# QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
# ANSWERS = 'sample_data/answer.csv'
# ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
#
#
# def open_file(csv_file):
#     data = []
#     with open(csv_file, 'r') as file:
#         content = csv.DictReader(file)
#         for row in content:
#             data.append(row)
#     return data
#
#
# def add_new_question(questions):
#     with open('sample_data/question.csv', 'w') as file:
#         writer = csv.DictWriter(file, fieldnames=QUESTION_HEADER)
#         writer.writeheader()
#         for question in questions:
#             writer.writerow(
#                 {'id': question['id'], 'submission_time': question['submission_time'],
#                  'view_number': question['view_number'], 'vote_number': question['vote_number'],
#                  'title': question['title'], 'message': question['message'], 'image': question['image']})
#
#
# def add_new_answer(answers):
#     with open('sample_data/answer.csv', 'w') as file:
#         writer = csv.DictWriter(file, fieldnames=ANSWER_HEADER)
#         writer.writeheader()
#         for answer in answers:
#             writer.writerow({'id': answer['id'], 'submission_time': answer['submission_time'],
#                              'vote_number': answer['vote_number'], 'question_id': answer['question_id'],
#                              'message': answer['message'], 'image': answer['image']})
#
#
# def save_image(app):
#     file = request.files['image']
#     filename = secure_filename(file.filename)
#     if file.filename != '':
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     return filename
#

@connection.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()
