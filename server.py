from flask import Flask, render_template, redirect, request, url_for, session, flash
import os
import data_manager
import util

UPLOAD_FOLDER = 'static/Images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
@app.route("/list")
def index():
    if 'username' in session:
        user_id = data_manager.get_id_of_user()[0]['id']
        if request.path == '/':
            questions, sort_types, directions = util.sorter(data_manager.get_latest_questions)
            return render_template('index.html', questions=questions, latest_questions=questions, user_id=user_id)
        else:
            questions, sort_types, directions = util.sorter(data_manager.get_questions)
        return render_template('index.html', questions=questions, sort_types=sort_types.keys(),
                               directions=directions.keys(), user_id=user_id)
    else:
        if request.path == '/':
            questions, sort_types, directions = util.sorter(data_manager.get_latest_questions)
            return render_template('index.html', questions=questions, latest_questions=questions)
        else:
            questions, sort_types, directions = util.sorter(data_manager.get_questions)
        return render_template('index.html', questions=questions, sort_types=sort_types.keys(),
                               directions=directions.keys())


@app.route('/question', methods=['GET', 'POST'])
def add_question():
    submission_time = util.get_submission_time()
    user_id = data_manager.get_id_of_user()[0]['id']
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        question = {'submission_time': submission_time, 'view_number': 0, 'vote_number': 0,
                    'title': request.form['title'], 'message': request.form['message'],
                    'image': filename, 'user_id': user_id}
        data_manager.add_new_question(question)
        new_id = data_manager.get_id()[0]['max']
        question_count = data_manager.get_question_count(user_id)[0]['question_count']
        data_manager.update_question_count(question_count + 1, user_id)
        return redirect(url_for('display', question_id=new_id))
    return render_template('question.html')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    question = data_manager.get_question(question_id)
    submission_time = util.get_submission_time()
    print(question[0]['user_id'])
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        updated_question = {'id': question_id, 'submission_time': submission_time,
                            'view_number': question[0]['view_number'], 'vote_number': question[0]['vote_number'],
                            'title': request.form['title'], 'message': request.form['message'],
                            'image': filename, 'user_id': question[0]['user_id']}
        data_manager.update_question(question_id, updated_question)
        return redirect(url_for('display', question_id=question_id))
    return render_template('question.html', question=question, question_id=int(question_id) - 1)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def update_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    submission_time = util.get_submission_time()
    question_id = answer[0]['question_id']
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        updated_answer = {'id': answer_id, 'submission_time': submission_time, 'vote_number': answer[0]['vote_number'],
                          'message': request.form['message-input'], 'image': filename, 'user_id': answer[0]['user_id']}
        data_manager.update_answer(answer_id, updated_answer)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-answer.html', answer=answer, answer_id=int(answer_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete_question_tag_by_question_id(question_id)
    data_manager.delete_comment_by_question_id(question_id)
    answers = data_manager.get_answers(question_id)
    for answer in answers:
        data_manager.delete_comment_by_answer_id(answer['id'])
        if answer['image'] != '':
            os.remove(f"static/Images/{answer['image']}")
    data_manager.delete_answer_by_question_id(question_id)
    question = data_manager.get_question(question_id)
    if question[0]['image'] != "":
        os.remove(f"static/Images/{question[0]['image']}")
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    question_id = answer[0]['question_id']
    if answer[0]['image'] != '':
        os.remove(f"static/Images/{answer[0]['image']}")
    data_manager.delete_answer(answer_id)
    return redirect(url_for('display', question_id=question_id))


@app.route('/question/<int:question_id>', methods=['GET'])
def display(question_id):
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers(question_id)
    question_comments = data_manager.get_question_comments(question_id)
    answer_comments = data_manager.get_comments()
    view_number = question[0]['view_number'] + 1
    updated_question = {'id': question_id, 'submission_time': question[0]['submission_time'], 'view_number': view_number,
                        'vote_number': question[0]['vote_number'], 'title': question[0]['title'],
                        'message': question[0]['message'], 'image': question[0]['image'], 'user_id': question[0]['user_id']}
    data_manager.update_question(question_id, updated_question)
    question_tags = data_manager.get_question_tags(question_id)
    return render_template('details.html', question=question, answers=answers, question_comments=question_comments,
                           answer_comments=answer_comments, question_tags=question_tags)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        new_answer = {'submission_time': submission_time, 'vote_number': 0, 'question_id': question_id,
                      'message': request.form['message-input'], 'image': filename,
                      'user_id': data_manager.get_id_of_user()[0]['id']}
        data_manager.add_new_answer(new_answer)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-answer.html')


@app.route('/question/<int:question_id>/vote_up')
@app.route('/question/<int:question_id>/vote_down')
def update_question_vote(question_id):
    question = data_manager.get_question(question_id)
    current_vote = question[0]['vote_number']
    current_reputation = data_manager.get_reputation(question[0]['user_id'])
    if request.path == '/question/' + str(question_id) + '/vote_up':
        current_vote += 1
        new_reputation = current_reputation[0]['reputation'] + 5
    else:
        current_vote -= 1
        new_reputation = current_reputation[0]['reputation'] - 2
    data_manager.update_question_vote(question_id, current_vote)
    data_manager.update_reputation(question[0]['user_id'], new_reputation)
    return redirect('/list')


@app.route('/answer/<int:answer_id>/vote_up')
@app.route('/answer/<int:answer_id>/vote_down')
def vote_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    current_vote = answer[0]['vote_number']
    current_reputation = data_manager.get_reputation(answer[0]['user_id'])
    if request.path == '/answer/' + str(answer_id) + '/vote_up':
        current_vote += 1
        new_reputation = current_reputation[0]['reputation'] + 10
    else:
        current_vote -= 1
        new_reputation = current_reputation[0]['reputation'] - 2
    data_manager.update_answer_vote(answer_id, current_vote)
    data_manager.update_reputation(answer[0]['user_id'], new_reputation)
    return redirect(url_for('display', question_id=answer[0]['question_id']))


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id):
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        new_comment = {'question_id': question_id, 'answer_id': None, 'message': request.form['comment_message'],
                       'submission_time': submission_time,
                       'edited_count': 0, 'user_id': data_manager.get_id_of_user()[0]['id']}
        data_manager.add_new_comment_to_question(new_comment)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-comment.html')


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(answer_id):
    submission_time = util.get_submission_time()
    question_id = data_manager.get_answer(answer_id)[0]['question_id']
    if request.method == 'POST':
        new_comment = {'question_id': question_id, 'answer_id': answer_id, 'message': request.form['comment_message'],
                       'submission_time': submission_time, 'edited_count': 0,
                       'user_id': data_manager.get_id_of_user()[0]['id']}
        data_manager.add_new_comment_to_answer(new_comment)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-comment.html')


@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment(comment_id)
    question_id = comment[0]['question_id']
    answer_id = comment[0]['answer_id']
    submission_time = util.get_submission_time()
    edited_count = comment[0]['edited_count'] + 1
    if request.method == 'POST':
        updated_comment = {'question_id': question_id, 'answer_id': answer_id,
                           'message': request.form['comment_message'],
                           'submission_time': submission_time,
                           'edited_count': edited_count, 'user_id': comment[0]['user_id']}
        data_manager.edit_comment(comment_id, updated_comment)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-comment.html', comment=comment)


@app.route('/comment/<int:comment_id>/delete')
def delete_comment(comment_id):
    comment = data_manager.get_comment(comment_id)
    question_id = comment[0]['question_id']
    data_manager.delete_comment(comment_id)
    return redirect(url_for('display', question_id=question_id))


@app.route('/question/<int:question_id>/new-tag', methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'POST':
        new_tag = {'name': request.form['tag']}
        all_tag_names = [tag_name['name'] for tag_name in data_manager.get_all_tags()]
        if new_tag['name'] in all_tag_names:
            tag_id = data_manager.get_tag_id_by_name(new_tag['name'])[0]['id']
            new_question_tag = {'question_id': question_id, 'tag_id': tag_id}
            data_manager.add_new_tag_to_question(new_question_tag)
        else:
            data_manager.add_new_tag(new_tag)
            tag_id = data_manager.get_tag_id_by_name(new_tag['name'])[0]['id']
            new_question_tag = {'question_id': question_id, 'tag_id': tag_id}
            data_manager.add_new_tag_to_question(new_question_tag)
        return redirect(url_for('display', question_id=question_id))
    all_tag = data_manager.get_all_tags()
    return render_template('add-tag.html', question_id=question_id, all_tag=all_tag)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_question_tag(tag_id, question_id)
    return redirect(url_for('display', question_id=question_id))


@app.route('/search')
def search():
    ids = []
    no_results = True
    search_phrase = request.args.get('search_phrase')
    questions = data_manager.highlight_questions(search_phrase)
    answers = data_manager.highlight_answers(search_phrase)
    searched_ids = data_manager.get_ids(data_manager.search_question(search_phrase), "question", ids)
    data_manager.get_ids(data_manager.search_answer(search_phrase), "answer", searched_ids)
    if searched_ids:
        no_results = False
    return render_template('search.html', searched_ids=searched_ids, questions=questions, no_results=no_results,
                           answer_ids=data_manager.get_answer_ids(data_manager.search_answer_ids(search_phrase)),
                           search_phrase=search_phrase, answers=answers)


@app.route('/tags')
def show_tags():
    show_tag = data_manager.get_all_used_tags()
    return render_template('tags.html', show_tag=show_tag)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_manager.get_password(username):
            if util.verify_password(password, data_manager.get_password(username)[0]['password']):
                session['username'] = username
                session['password'] = password
                session['logged_in'] = True
                flash('You were just logged in')
                return redirect(url_for('index'))
            else:
                error = 'Wrong password!'
                return render_template('login.html', error=error)
        else:
            error = 'Wrong username!'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    flash('You were just logged out')
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        submission_time = util.get_submission_time()
        password = util.hash_password(request.form['password'])
        user = {'name': request.form['username'], 'password': password, 'reg_date': submission_time,
                'question_count': 0, 'answer_count': 0, 'comment_count': 0, 'reputation': 0}
        data_manager.add_new_user(user)
        return redirect('/list')
    return render_template('registration.html')


@app.route('/users')
def users():
    list_of_users = data_manager.get_all_users()
    return render_template('users.html', users=list_of_users)


@app.route('/user/<user_id>')
def user_page(user_id):
    user = data_manager.get_all_users()[int(user_id) - 1]
    return render_template('user_page.html', user=user)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
