from flask import Flask, render_template, redirect, request, url_for

import data_manager
import util


app = Flask(__name__)


@app.route("/")
def index():
    questions = data_manager.open_file(data_manager.QUESTIONS)
    questions.reverse()
    dates = []
    for question in questions:
        dates.append(util.from_timestamp_to_time(int(question[1])))
    return render_template('index.html', header=data_manager.QUESTION_HEADER, questions=questions, dates=dates)


# @app.route('/list')
# def lister():
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     questions.reverse()
#     return render_template('list.html', questions=questions)


@app.route('/question', methods=['GET', 'POST'])
def add_question():
    questions = data_manager.open_file(data_manager.QUESTIONS)
    new_id = util.get_max_id(questions) + 1
    submission_time = util.get_submission_time()
    view_number, vote_number = 0, 0
    image = 'x'
    if request.method == 'POST':
        question = [new_id, submission_time, view_number, vote_number, request.form['title'], request.form['message'],
                    image]
        questions.append(question)
        data_manager.add_new_question(questions)
        return redirect(url_for('display', question_id=new_id))
    return render_template('question.html')


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def update_question(question_id):
    questions = data_manager.open_file(data_manager.QUESTIONS)
    submission_time = util.get_submission_time()
    if request.method == 'POST':
        for question in questions:
            if int(question[0]) == int(question_id):
                updated_question = [question_id, submission_time, question[2], question[3], request.form['title'],
                                    request.form['message'], question[6]]
                del questions[question_id - 1]
                questions.insert(question_id - 1, updated_question)
        data_manager.add_new_question(questions)
        return redirect(url_for('display', question_id=question_id))
    return render_template('question.html', questions=questions, question_id=int(question_id) - 1)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    questions = data_manager.open_file(data_manager.QUESTIONS)
    for question in questions:
        if int(question[0]) == int(question_id):
            del questions[questions.index(question)]
    data_manager.add_new_question(questions)
    return redirect('/')


@app.route('//answer/<answer_id>/delete')
def delete_answer(answer_id):
    answers = data_manager.open_file(data_manager.ANSWERS)
    for answer in answers:
        if int(answer[0]) == int(answer_id):
            question_id = answer[3]
            del answers[answers.index(answer)]
    data_manager.add_new_answer(answers)
    return redirect(url_for('display', question_id=question_id))


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    answers = data_manager.open_file(data_manager.ANSWERS)
    new_id = util.get_max_id(answers) + 1
    submission_time = util.get_submission_time()
    vote_number = 0
    image = 'x'
    if request.method == 'POST':
        new_answer = [new_id, submission_time, vote_number, question_id, request.form['message'], image]
        answers.insert(new_id, new_answer)
        data_manager.add_new_answer(answers)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-answer.html')


@app.route('/question/<int:question_id>', methods=['GET'])
def display(question_id):
    questions = data_manager.open_file(data_manager.QUESTIONS)
    answers = data_manager.open_file(data_manager.ANSWERS)
    for question in questions:
        if int(question[0]) == int(question_id):
            return render_template('id.html', question=question, answers=answers)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
