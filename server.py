from flask import Flask, render_template, redirect, request, url_for
import os
import data_manager
import util

UPLOAD_FOLDER = 'static/Images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    questions = data_manager.open_file(data_manager.QUESTIONS)
    questions.reverse()
    dates = []
    for question in questions:
        dates.append(util.from_timestamp_to_time(int(question[1])))
    sort_types = ['Title', 'Submission Time', 'Message', 'Number of views', 'Number of votes']
    sorting = request.args.get('sorting')
    directions = ['Ascending', 'Descending']
    sorting_direction = request.args.get('sorting_direction')
    if sorting is not None:
        questions = util.sorter(sorting, sorting_direction, questions)
    return render_template('index.html', header=data_manager.QUESTION_HEADER, questions=questions, dates=dates,
                           sorting=sorting, sorting_direction=sorting_direction, directions=directions,
                           sort_types=sort_types)


@app.route('/question', methods=['GET', 'POST'])
def add_question():
    questions = data_manager.open_file(data_manager.QUESTIONS)
    new_id = util.get_max_id(questions) + 1
    submission_time = util.get_submission_time()
    view_number, vote_number = 0, 0
    if request.method == 'POST':
        filename = util.save_image(app)
        question = [new_id, submission_time, view_number, vote_number, request.form['title'], request.form['message'],
                    filename]
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
                filename = util.save_image(app)
                updated_question = [question_id, submission_time, question[2], question[3], request.form['title'],
                                    request.form['message'], filename]
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
            if question[6] != "":
                os.remove(f"static/Images/{questions[questions.index(question)][6]}")
            del questions[questions.index(question)]
    data_manager.add_new_question(questions)
    return redirect('/')


@app.route('//answer/<answer_id>/delete')
def delete_answer(answer_id):
    answers = data_manager.open_file(data_manager.ANSWERS)
    for answer in answers:
        if int(answer[0]) == int(answer_id):
            question_id = answer[3]
            if answer[5] != '':
                os.remove(f"static/Images/{answers[answers.index(answer)][5]}")
            del answers[answers.index(answer)]
    data_manager.add_new_answer(answers)
    return redirect(url_for('display', question_id=question_id))


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    answers = data_manager.open_file(data_manager.ANSWERS)
    new_id = util.get_max_id(answers) + 1
    submission_time = util.get_submission_time()
    vote_number = 0
    if request.method == 'POST':
        filename = util.save_image(app)
        new_answer = [new_id, submission_time, vote_number, question_id, request.form['message'], filename]
        answers.insert(new_id, new_answer)
        data_manager.add_new_answer(answers)
        return redirect(url_for('display', question_id=question_id))
    return render_template('new-answer.html')


@app.route('/question/<int:question_id>', methods=['GET'])
def display(question_id):
    questions = data_manager.open_file(data_manager.QUESTIONS)
    answers = data_manager.open_file(data_manager.ANSWERS)
    dates = {}
    for answer in answers:
        if answer[3] in dates:
            dates[answer[3]].append(util.from_timestamp_to_time(int(answer[1])))
        else:
            dates[answer[3]] = [util.from_timestamp_to_time(int(answer[1]))]
    for question in questions:
        if int(question[0]) == int(question_id):
            return render_template('id.html', question=question, answers=answers, dates=dates)


@app.route('/question/<int:question_id>/vote_up')
@app.route('/question/<int:question_id>/vote_down')
def vote(question_id):
    questions = data_manager.open_file(data_manager.QUESTIONS)
    for question in questions:
        if int(question[0]) == int(question_id):
            if request.path == '/question/' + str(question_id) + '/vote_up':
                question[3] = int(question[3]) + 1
            else:
                question[3] = int(question[3]) - 1
            data_manager.add_new_question(questions)
            return redirect('/')


@app.route('/answer/<int:answer_id>/vote_up')
@app.route('/answer/<int:answer_id>/vote_down')
def vote_answer(answer_id):
    answers = data_manager.open_file(data_manager.ANSWERS)
    for answer in answers:
        if int(answer[0]) == int(answer_id):
            question_id = answer[3]
            if request.path == '/answer/' + str(answer_id) + '/vote_up':
                answer[2] = int(answer[2]) + 1
            else:
                answer[2] = int(answer[2]) - 1
            data_manager.add_new_answer(answers)
            return redirect(url_for('display', question_id=question_id))


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
