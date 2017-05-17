'''
data manager for AskMate
persists data in postgres database
by SzószKód
'''

import os
import datetime
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
    submitted_answer = dict(answer)
    submitted_answer['submission_time'] = datetime.datetime.fromtimestamp(submitted_answer['submission_time'])
    query = "UPDATE answer \
             SET submission_time = %(submission_time)s, vote_number = %(vote_number)s, \
             message = %(message)s, image = %(image)s WHERE id = %(id)s"
    DatabaseConnection._cursor.execute(query, submitted_answer)


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
