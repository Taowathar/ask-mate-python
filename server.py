from flask import Flask, render_template, redirect, request, url_for
import os
import data_manager
import util

UPLOAD_FOLDER = 'static/Images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    sort_types = {'Title': 'title', 'Submission Time': 'submission_time', 'Message': 'message', 'Number of views': 'view_number', 'Number of votes': 'vote_number'}
    directions = {'Ascending': 'ASC', 'Descending': 'DESC'}
    sorting = request.args.get('sorting')
    sorting_direction = request.args.get('sorting_direction')
    if sorting is not None:
        questions = data_manager.get_questions(sort_types[sorting], directions[sorting_direction])
    else:
        sorting = 'submission_time'
        sorting_direction = 'DESC'
        questions = data_manager.get_questions(sorting, sorting_direction)
    return render_template('index.html', questions=questions, sort_types=sort_types.keys(), directions=directions.keys())


@app.route('/question', methods=['GET', 'POST'])
def add_question():
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        question = {'submission_time': submission_time, 'view_number': 0, 'vote_number': 0,
                    'title': request.form['title'], 'message': request.form['message'], 'image': filename}
        data_manager.add_new_question(question)
        new_id = data_manager.get_id()[0]['max']
        return redirect(url_for('display', question_id=new_id))
    return render_template('question.html')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    question = data_manager.get_question(question_id)
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        updated_question = {'id': question_id, 'submission_time': submission_time,
                            'view_number': question[0]['view_number'], 'vote_number': question[0]['vote_number'],
                            'title': request.form['title'], 'message': request.form['message'],
                            'image': filename}
        data_manager.update_question(question_id, updated_question)
        return redirect(url_for('display', question_id=question_id))
    return render_template('question.html', question=question, question_id=int(question_id) - 1)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    question = data_manager.get_question(question_id)
    if question[0]['image'] != "":
        os.remove(f"static/Images/{question[0]['image']}")
    data_manager.delete_question(question_id)
    return redirect('/')


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
    return render_template('details.html', question=question, answers=answers)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        filename = data_manager.save_image(app)
        new_answer = {'submission_time': submission_time, 'vote_number': 0, 'question_id': question_id,
                      'message': request.form['message'], 'image': filename}
        data_manager.add_new_answer(new_answer)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-answer.html')


@app.route('/question/<int:question_id>/vote_up')
@app.route('/question/<int:question_id>/vote_down')
def update_question_vote(question_id):
    question = data_manager.get_question(question_id)
    current_vote = question[0]['vote_number']
    if request.path == '/question/' + str(question_id) + '/vote_up':
        current_vote += 1
    else:
        current_vote -= 1
    data_manager.update_question_vote(question_id, current_vote)
    return redirect('/')


@app.route('/answer/<int:answer_id>/vote_up')
@app.route('/answer/<int:answer_id>/vote_down')
def vote_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    current_vote = answer[0]['vote_number']
    if request.path == '/answer/' + str(answer_id) + '/vote_up':
        current_vote += 1
    else:
        current_vote -= 1
    data_manager.update_answer_vote(answer_id, current_vote)
    return redirect(url_for('display', question_id=answer[0]['question_id']))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
