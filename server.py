from flask import Flask, render_template, redirect, request, url_for
import os
import data_manager
import util

# UPLOAD_FOLDER = 'static/Images'

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route("/")
# def index():
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     questions.reverse()
#     dates = []
#     for question in questions:
#         dates.append(util.from_timestamp_to_time(int(question['submission_time'])))
#     sort_types = ['Title', 'Submission Time', 'Message', 'Number of views', 'Number of votes']
#     sorting = request.args.get('sorting')
#     directions = ['Ascending', 'Descending']
#     sorting_direction = request.args.get('sorting_direction')
#     if sorting is not None:
#         questions = util.sorter(sorting, sorting_direction, questions)
#     return render_template('index.html', header=data_manager.QUESTION_HEADER, questions=questions, dates=dates,
#                            sorting=sorting, sorting_direction=sorting_direction, directions=directions,
#                            sort_types=sort_types)
#
#
# @app.route('/question', methods=['GET', 'POST'])
# def add_question():
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     new_id = util.get_max_id(questions) + 1
#     submission_time = util.get_submission_time()
#     if request.method == 'POST':
#         filename = data_manager.save_image(app)
#         question = {'id': new_id, 'submission_time': submission_time, 'view_number': 0, 'vote_number': 0,
#                     'title': request.form['title'], 'message': request.form['message'], 'image': filename}
#         questions.append(question)
#         data_manager.add_new_question(questions)
#         return redirect(url_for('display', question_id=new_id))
#     return render_template('question.html')
#
#
# @app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
# def update_question(question_id):
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     submission_time = util.get_submission_time()
#     if request.method == 'POST':
#         for question in questions:
#             if int(question['id']) == int(question_id):
#                 filename = data_manager.save_image(app)
#                 updated_question = {'id': question_id, 'submission_time': submission_time,
#                                     'view_number': question['view_number'], 'vote_number': question['vote_number'],
#                                     'title': request.form['title'], 'message': request.form['message'],
#                                     'image': filename}
#                 del questions[question_id - 1]
#                 questions.insert(question_id - 1, updated_question)
#         data_manager.add_new_question(questions)
#         return redirect(url_for('display', question_id=question_id))
#     return render_template('question.html', questions=questions, question_id=int(question_id) - 1)
#
#
# @app.route('/question/<question_id>/delete')
# def delete_question(question_id):
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     for question in questions:
#         if int(question['id']) == int(question_id):
#             if question['image'] != "":
#                 os.remove(f"static/Images/{questions[questions.index(question)]['image']}")
#             del questions[questions.index(question)]
#     data_manager.add_new_question(questions)
#     return redirect('/')
#
#
# @app.route('//answer/<answer_id>/delete')
# def delete_answer(answer_id):
#     answers = data_manager.open_file(data_manager.ANSWERS)
#     for answer in answers:
#         if int(answer['id']) == int(answer_id):
#             question_id = answer['question_id']
#             if answer['image'] != '':
#                 os.remove(f"static/Images/{answers[answers.index(answer)]['image']}")
#             del answers[answers.index(answer)]
#     data_manager.add_new_answer(answers)
#     return redirect(url_for('display', question_id=question_id))
#
#
# @app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
# def add_answer(question_id):
#     answers = data_manager.open_file(data_manager.ANSWERS)
#     new_id = util.get_max_id(answers) + 1
#     submission_time = util.get_submission_time()
#     if request.method == 'POST':
#         filename = data_manager.save_image(app)
#         new_answer = {'id': new_id, 'submission_time': submission_time,'vote_number': 0, 'question_id': question_id,
#                       'message': request.form['message'], 'image': filename}
#         answers.insert(new_id, new_answer)
#         data_manager.add_new_answer(answers)
#         return redirect(url_for('display', question_id=question_id))
#     return render_template('new-answer.html')
#
#
# @app.route('/question/<int:question_id>', methods=['GET'])
# def display(question_id):
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     answers = data_manager.open_file(data_manager.ANSWERS)
#     dates = {}
#     for answer in answers:
#         if answer['question_id'] in dates:
#             dates[answer['question_id']].append(util.from_timestamp_to_time(int(answer['submission_time'])))
#         else:
#             dates[answer['question_id']] = [util.from_timestamp_to_time(int(answer['submission_time']))]
#     for question in questions:
#         if int(question['id']) == int(question_id):
#             return render_template('details.html', question=question, answers=answers, dates=dates)
#
#
# @app.route('/question/<int:question_id>/vote_up')
# @app.route('/question/<int:question_id>/vote_down')
# def vote(question_id):
#     questions = data_manager.open_file(data_manager.QUESTIONS)
#     for question in questions:
#         if int(question['id']) == int(question_id):
#             if request.path == '/question/' + str(question_id) + '/vote_up':
#                 question['vote_number'] = int(question['vote_number']) + 1
#             else:
#                 question['vote_number'] = int(question['vote_number']) - 1
#             data_manager.add_new_question(questions)
#             return redirect('/')
#
#
# @app.route('/answer/<int:answer_id>/vote_up')
# @app.route('/answer/<int:answer_id>/vote_down')
# def vote_answer(answer_id):
#     answers = data_manager.open_file(data_manager.ANSWERS)
#     for answer in answers:
#         if int(answer['id']) == int(answer_id):
#             question_id = answer['question_id']
#             if request.path == '/answer/' + str(answer_id) + '/vote_up':
#                 answer['vote_number'] = int(answer['vote_number']) + 1
#             else:
#                 answer['vote_number'] = int(answer['vote_number']) - 1
#             data_manager.add_new_answer(answers)
#             return redirect(url_for('display', question_id=question_id))


@app.route("/")
def index():
    questions = data_manager.get_questions()
    return render_template('index.html', questions=questions)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
