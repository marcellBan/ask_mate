'''
data manager for AskMate
persists data in postgres database
by SzószKód
'''

import csv
import os
import base64
import psycopg2
from constants import (QUESTIONS_FILE, ANSWERS_FILE,
                       QUESTION_FIELDS, ANSWER_FIELDS,
                       ENCODE_QUESTION_FIELDS, ENCODE_ANSWER_FIELDS,
                       CONVERT_QUESTION_FIELDS, CONVERT_ANSWER_FIELDS)


class DatabaseConnection(object):
    _db_connection = None
    _cursor = None

    @staticmethod
    def connect_to_database():
        connection_data = {
            'dbname': os.environ.get('MY_PSQL_DBNAME'),
            'user': os.environ.get('MY_PSQL_USER'),
            'host': os.environ.get('MY_PSQL_HOST'),
            'password': os.environ.get('MY_PSQL_PASSWORD')
        }
        connect_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect_string = connect_string.format(**connection_data)
        DatabaseConnection._db_connection = psycopg2.connect(connect_string)
        DatabaseConnection._db_connection.autocommit = True
        DatabaseConnection._cursor = DatabaseConnection._db_connection.cursor()

    @staticmethod
    def close_database_connection():
        if DatabaseConnection._cursor is not None:
            DatabaseConnection._cursor.close()
        if DatabaseConnection._db_connection is not None:
            DatabaseConnection._db_connection.close()


def get_question(question_id):
    DatabaseConnection._cursor.execute('''SELECT * FROM question WHERE id = %s;''', [question_id])
    question = DatabaseConnection._cursor.fetchall()[0]
    dict_of_question = {'id': question[0],
                        'submission_time': question[1].timestamp(),
                        'view_number': question[2],
                        'vote_number': question[3],
                        'title': question[4],
                        'message': question[5],
                        'image': question[6]}
    return dict_of_question


def get_questions(sorting=None, limit=None):
    DatabaseConnection._cursor.execute('''SELECT * FROM question''')
    questions = DatabaseConnection._cursor.fetchall()
    questions = construct_question_dicts(questions)
    return questions


def get_answers(question_id):
    DatabaseConnection._cursor.execute('''SELECT * FROM answer WHERE id = %s;''', [question_id])
    answers = DatabaseConnection._cursor.fetchall()
    answers = construct_answer_dicts(answers)
    return answers


def new_question(question):
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = "INSERT INTO question (submission_time, view_number, vote_number, title, message, image) \
             VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);"
    DatabaseConnection._cursor.execute(query, final_question)


def new_answer(answer):
    final_answer = dict(answer)
    final_answer['submission_time'] = datetime.datetime.fromtimestamp(final_answer['submission_time'])
    query = "INSERT INTO answer (submission_time, vote_number, question_id, message, image) \
             VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);"
    DatabaseConnection._cursor.execute(query, final_answer)


def update_question(question):
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = "UPDATE question \
             SET submission_time = %(submission_time)s, vote_number = %(vote_number)s, \
             message = %(message)s, image = %(image)s WHERE id = %(id)s"
    DatabaseConnection._cursor.execute(query, final_question)


def update_answer(answer):
    pass


def delete_question(question_id):
    pass


def delete_answer(answer_id):
    pass


def construct_question_dicts(result_set):
    questions = dict()
    for question in result_set:
        questions[question[0]] = {
            'id': question[0],
            'submission_time': question[1].timestamp(),
            'view_number': question[2],
            'vote_number': question[3],
            'title': question[4],
            'message': question[5],
            'image': question[6]
        }
    return questions


def construct_answer_dicts(result_set):
    answers = dict()
    for answer in result_set:
        answers[answer[0]] = {
            'id': answer[0],
            'submission_time': answer[1].timestamp(),
            'vote_number': answer[2],
            'message': answer[3],
            'image': answer[4]
        }
    return answers

# FIXME: Deprecated TODO: complete rewrite


def load_data(answers=False):
    '''returns a dict of dicts containing the current data in the appropriate file'''
    data = dict()
    if answers:
        filepath = ANSWERS_FILE
        fields = ANSWER_FIELDS
        decode = ENCODE_ANSWER_FIELDS
        convert = CONVERT_ANSWER_FIELDS
    else:
        filepath = QUESTIONS_FILE
        fields = QUESTION_FIELDS
        decode = ENCODE_QUESTION_FIELDS
        convert = CONVERT_QUESTION_FIELDS
    if os.path.isfile(filepath):
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=',')
            for row in reader:
                row['id'] = int(row['id'])
                for field in decode:
                    row[field] = base64.b64decode(row[field]).decode()
                for con in convert:
                    row[con[0]] = con[1](row[con[0]])
                data[row['id']] = row
    return data


def save_data(data, answers=False):
    '''saves a dict of dicts to the appropriate file'''
    if answers:
        filepath = ANSWERS_FILE
        fields = ANSWER_FIELDS
        encode = ENCODE_ANSWER_FIELDS
    else:
        filepath = QUESTIONS_FILE
        fields = QUESTION_FIELDS
        encode = ENCODE_QUESTION_FIELDS
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=',')
        for row in data:
            for field in encode:
                data[row][field] = base64.b64encode(bytearray(data[row][field], encoding='utf-8')).decode()
            writer.writerow(data[row])

if __name__ == '__main__':
    DatabaseConnection.connect_to_database()
    DatabaseConnection._cursor.execute('SELECT * FROM answer')
    print(DatabaseConnection._cursor.fetchall())
    DatabaseConnection.close_database_connection()
