import csv

QUESTIONS = 'sample_data/question.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS = 'sample_data/answer.csv'


def open_file(files):
    datas = []
    with open(files, 'r') as file:
        content = csv.DictReader(file)
        for row in content:
            data = []
            for item in row:
                if item == 'image':
                    data.append(row[item])
                    break
                data.append(row[item])
            datas.append(data)
    return datas


def add_new_question(questions):
    with open('sample_data/question.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=QUESTION_HEADER)
        writer.writeheader()
        for question in questions:
            writer.writerow(
                {'id': question[0], 'submission_time': question[1], 'view_number': question[2],
                 'vote_number': question[3], 'title': question[4], 'message': question[5], 'image': question[6]})



