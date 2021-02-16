# import csv
import os
from werkzeug.utils import secure_filename
from flask import request


import connection
from psycopg2.extras import RealDictCursor


def save_image(app):
    file = request.files['image']
    filename = secure_filename(file.filename)
    if file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename


@connection.connection_handler
def get_questions(cursor: RealDictCursor, sort: str, direction: str) -> list:
    query = f"""
        SELECT *
        FROM question
        ORDER BY {sort} {direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor: RealDictCursor, question: dict) -> list:
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)"""
    cursor.execute(query, question)


@connection.connection_handler
def add_new_answer(cursor: RealDictCursor, answer) -> list:
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)"""
    cursor.execute(query, answer)


@connection.connection_handler
def get_question(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT *
        FROM question
        WHERE id = {question_id}"""
    cursor.execute(query)
    return cursor.fetchall()



@connection.connection_handler
def get_answers(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {question_id}
        ORDER BY submission_time DESC"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answer(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
        SELECT *
        FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_id(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT MAX(id)
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_question(cursor: RealDictCursor, question_id, updated_question) -> list:
    query = f"""
        UPDATE question
        SET submission_time = '{updated_question['submission_time']}',
        view_number = '{updated_question['view_number']}',
        vote_number = '{updated_question['vote_number']}',
        title = '{updated_question['title']}',
        message = '{updated_question['message']}',
        image = '{updated_question['image']}'
        WHERE id = {question_id}"""
    cursor.execute(query)


@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        DELETE FROM question
        WHERE id = {question_id};
        DELETE FROM answer
        WHERE question_id = {question_id}"""
    cursor.execute(query)


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id) -> list:
    query = f"""
        DELETE FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)


@connection.connection_handler
def update_question_vote(cursor: RealDictCursor, question_id, updated_vote) -> list:
    query = f"""
        UPDATE question
        SET vote_number = {updated_vote}
        WHERE id = {question_id}"""
    cursor.execute(query)


@connection.connection_handler
def update_answer_vote(cursor: RealDictCursor, answer_id, updated_vote) -> list:
    query = f"""
        UPDATE answer
        SET vote_number = {updated_vote}
        WHERE id = {answer_id}"""
    cursor.execute(query)