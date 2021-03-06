import os
from werkzeug.utils import secure_filename
from flask import request, session


import connection
from psycopg2.extras import RealDictCursor


def save_image(app):
    file = request.files['image']
    filename = secure_filename(file.filename)
    if file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename


@connection.connection_handler
def get_all_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_questions(cursor: RealDictCursor, sort: str, direction: str) -> list:
    query = f"""
        SELECT *
        FROM question
        ORDER BY {sort} {direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_latest_questions(cursor: RealDictCursor, sort: str, direction: str) -> list:
    query = f"""
        SELECT *
        FROM question
        ORDER BY {sort} {direction}
        LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_question(cursor: RealDictCursor, question: dict) -> list:
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
        VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s)
        """
    cursor.execute(query, question)


@connection.connection_handler
def add_new_answer(cursor: RealDictCursor, answer) -> list:
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
        VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s)
        """
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
    query = """
        SELECT MAX(id)
        FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_question(cursor: RealDictCursor, question_id, updated_question) -> list:
    query = f"""
        UPDATE question
        SET submission_time = %(submission_time)s,
        view_number = %(view_number)s,
        vote_number = %(vote_number)s,
        title = %(title)s,
        message = %(message)s,
        image = %(image)s,
        user_id = %(user_id)s
        WHERE id = {question_id}"""
    cursor.execute(query, updated_question)


@connection.connection_handler
def update_answer(cursor: RealDictCursor, answer_id, updated_answer) -> list:
    query = f"""
        UPDATE answer
        SET submission_time = %(submission_time)s,
        vote_number = %(vote_number)s,
        message = %(message)s,
        image = %(image)s,
        user_id = %(user_id)s
        WHERE id = {answer_id}"""
    cursor.execute(query, updated_answer)


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


@connection.connection_handler
def add_new_comment_to_question(cursor: RealDictCursor, comment) -> list:
    query = """
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
        VALUES (%(question_id)s, %(answer_id)s,%(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s)"""
    cursor.execute(query, comment)


@connection.connection_handler
def get_question_comments(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT *
        FROM comment
        WHERE question_id = {question_id} AND answer_id is null """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_comment_to_answer(cursor: RealDictCursor, comment) -> list:
    query = """
        INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count, user_id)
        VALUES (%(question_id)s, %(answer_id)s,%(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s)"""
    cursor.execute(query, comment)


@connection.connection_handler
def get_comments(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comment(cursor: RealDictCursor, comment_id) -> list:
    query = f"""
        SELECT *
        FROM comment
        WHERE id = {comment_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def edit_comment(cursor: RealDictCursor, comment_id, updated_comment) -> list:
    query = f"""
        UPDATE comment
        SET message = %(message)s,
        submission_time = %(submission_time)s,
        edited_count = %(edited_count)s,
        user_id = %(user_id)s
        WHERE id = {comment_id}"""
    cursor.execute(query, updated_comment)


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id) -> list:
    query = f"""
        DELETE FROM comment
         WHERE id = {comment_id}"""
    cursor.execute(query)


@connection.connection_handler
def add_new_tag(cursor: RealDictCursor, tag) -> list:
    query = """
        INSERT INTO tag (name)
        VALUES (%(name)s)"""
    cursor.execute(query, tag)


@connection.connection_handler
def add_new_tag_to_question(cursor: RealDictCursor, question_tag) -> list:
    query = """
        INSERT INTO question_tag (question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)"""
    cursor.execute(query, question_tag)


@connection.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM tag
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_names(cursor: RealDictCursor) -> list:
    query = """
        SELECT name
        FROM tag
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_tags(cursor: RealDictCursor, question_id) -> list:
    query = f"""
        SELECT *
        FROM question_tag
        JOIN tag
        ON tag.id = question_tag.tag_id
        WHERE question_id ={question_id}
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tag_id_by_name(cursor: RealDictCursor, tag_name) -> list:
    query = """
        SELECT id
        FROM tag
        WHERE name = %(tag_name)s"""
    cursor.execute(query, {'tag_name': tag_name})
    return cursor.fetchall()


@connection.connection_handler
def delete_question_tag(cursor: RealDictCursor, tag_id, question_id) -> list:
    query = f"""
        DELETE FROM question_tag
         WHERE tag_id = {tag_id} AND question_id = {question_id}"""
    cursor.execute(query)


@connection.connection_handler
def delete_answer_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        DELETE FROM answer
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def delete_comment_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        DELETE FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def delete_comment_by_answer_id(cursor: RealDictCursor, answer_id) -> list:
    query = """
        DELETE FROM comment
        WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def delete_question_tag_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = """
        DELETE FROM question_tag
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def get_all_used_tags(cursor: RealDictCursor) -> list:
    query = """
            SELECT name, count(tag_id) AS usage
            FROM question_tag
            JOIN tag ON tag.id=question_tag.tag_id
            GROUP BY name"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search_question(cursor: RealDictCursor, search_phrase) -> list:
    query = f"""
        SELECT id
        FROM question
        WHERE title LIKE '%{search_phrase}%'
        OR message LIKE '%{search_phrase}%'
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search_answer(cursor: RealDictCursor, search_phrase) -> list:
    query = f"""
        SELECT question_id
        FROM answer
        WHERE message LIKE '%{search_phrase}%'
        """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def search_answer_ids(cursor: RealDictCursor, search_phrase) -> list:
    query = f"""
        SELECT id
        FROM answer
        WHERE message LIKE '%{search_phrase}%'
        """
    cursor.execute(query)
    return cursor.fetchall()


def get_ids(id_list, id_type, ids):
    for item in id_list:
        if id_type == "question":
            ids.append(item['id'])
        else:
            ids.append(item['question_id'])
    return ids


def get_answer_ids(id_list):
    ids = []
    for item in id_list:
        ids.append(item['id'])
    return ids


def highlight_words_message(sentence_list, phrase):
    for sentence in sentence_list:
        sentence['message'] = sentence['message'].replace(phrase, f"<mark>{phrase}</mark>")
    return sentence_list


def highlight_words_title(sentence_list, phrase):
    for sentence in sentence_list:
        sentence['title'] = sentence['title'].replace(phrase, f"<mark>{phrase}</mark>")
    return sentence_list


def highlight_questions(search_phrase):
    questions = highlight_words_title(get_questions('submission_time', 'DESC'), search_phrase)
    return highlight_words_message(questions, search_phrase)


def highlight_answers(search_phrase):
    return highlight_words_message(get_all_answers(), search_phrase)


@connection.connection_handler
def get_password(cursor: RealDictCursor, username) -> list:
    query = """SELECT password FROM users
        WHERE name = %(name)s"""
    cursor.execute(query, {'name': username})
    return cursor.fetchall()


@connection.connection_handler
def add_new_user(cursor: RealDictCursor, user) -> list:
    query = """
        INSERT INTO users (name, password, reg_date, question_count, answer_count, comment_count, reputation)
        VALUES (%(name)s, %(password)s, %(reg_date)s, %(question_count)s, %(answer_count)s, %(comment_count)s,
        %(reputation)s)"""
    cursor.execute(query, user)


@connection.connection_handler
def get_id_of_user(cursor: RealDictCursor) -> list:
    query = """
        SELECT id
        FROM users
        WHERE name = %(name)s
        """
    cursor.execute(query, {'name': session['username']})
    return cursor.fetchall()


@connection.connection_handler
def get_all_users(cursor: RealDictCursor) -> list:
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_user_by_id(cursor: RealDictCursor, user_id) -> list:
    query = "SELECT * FROM users WHERE id = %(user_id)s"
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_reputation(cursor: RealDictCursor, user_id) -> list:
    query = f"""
        SELECT reputation
        FROM users
        WHERE id = {user_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_reputation(cursor: RealDictCursor, user_id, reputation) -> list:
    query = f"""
        UPDATE users
        SET reputation = {reputation}
        WHERE id = {user_id}"""
    cursor.execute(query)


@connection.connection_handler
def get_question_count(cursor: RealDictCursor, user_id):
    query = "SELECT question_count FROM users WHERE id = %(user_id)s"
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def update_question_count(cursor: RealDictCursor, question_count, user_id) -> list:
    query = """
        UPDATE users
        SET question_count = %(question_count)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'question_count': question_count, 'id': user_id})


@connection.connection_handler
def get_answer_count(cursor: RealDictCursor, user_id):
    query = "SELECT answer_count FROM users WHERE id = %(user_id)s"
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def update_answer_count(cursor: RealDictCursor, answer_count, user_id) -> list:
    query = """
        UPDATE users
        SET answer_count = %(answer_count)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'answer_count': answer_count, 'id': user_id})


@connection.connection_handler
def get_comment_count(cursor: RealDictCursor, user_id):
    query = "SELECT comment_count FROM users WHERE id = %(user_id)s"
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def update_comment_count(cursor: RealDictCursor, comment_count, user_id) -> list:
    query = """
        UPDATE users
        SET comment_count = %(comment_count)s
        WHERE id = %(id)s"""
    cursor.execute(query, {'comment_count': comment_count, 'id': user_id})


@connection.connection_handler
def get_user_questions(cursor: RealDictCursor, user_id) -> list:
    query = """
    SELECT * FROM question
    WHERE user_id = %(user_id)s
    ORDER BY submission_time DESC"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_user_answers(cursor: RealDictCursor, user_id) -> list:
    query = """
        SELECT * FROM answer
        WHERE user_id = %(user_id)s
        ORDER BY submission_time DESC"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_user_comments(cursor: RealDictCursor, user_id) -> list:
    query = """
        SELECT * FROM comment
        WHERE user_id = %(user_id)s
        ORDER BY submission_time DESC"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def remove_accepted_answer(cursor: RealDictCursor, answer_id) -> list:
    query = """
                UPDATE answer 
                SET accepted = false 
                WHERE id= %(answer_id)s"""
    cursor.execute(query,{'answer_id':answer_id})


@connection.connection_handler
def accepted_answer(cursor: RealDictCursor, answer_id) -> list:
    query = """
                UPDATE answer 
                SET accepted = true
                WHERE id= %(answer_id)s"""
    cursor.execute(query,{'answer_id':answer_id})

@connection.connection_handler
def get_username_by_question_id(cursor: RealDictCursor, question_id) -> list:
    query = f"""
            SELECT users.name 
            FROM users
            JOIN question 
            ON users.id=question.user_id
            WHERE question.id={question_id}"""
    cursor.execute(query)
    return cursor.fetchall()