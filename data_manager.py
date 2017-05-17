'''
data manager for AskMate
persists data in postgres database
by SzószKód
'''

import os
import datetime
import psycopg2


# TODO: do we want to change to a per query based connection system?
class DatabaseConnection(object):
    '''static class for handling one database connection'''
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
    '''returns a dictionary containing all the information of a question with the given id'''
    DatabaseConnection._cursor.execute("SELECT * FROM question WHERE id = %s;", [question_id])
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
    '''
    returns a dictionary of dictionaries containing all the questions\n
    the amount of questions returened can be limited with the limit parameter\n
    the sorting parameter is should be None or a list of tuples containing the column and the sorting order
    '''
    if sorting is None:
        DatabaseConnection._cursor.execute("SELECT * FROM question ORDER BY submission_time DESC;")
        questions = DatabaseConnection._cursor.fetchall()
        questions = construct_question_dicts(questions)
        return questions
    else:
        pass


def get_answer(answer_id):
    '''returns a dictionary containing all the information of an answer with the given id'''
    DatabaseConnection._cursor.execute("SELECT * FROM answer WHERE id = %s;", [answer_id])
    answer = DatabaseConnection._cursor.fetchall()[0]
    dict_of_answer = {'id': answer[0],
                      'submission_time': answer[1].timestamp(),
                      'vote_number': answer[2],
                      'question_id': answer[3],
                      'message': answer[4],
                      'image': answer[5]}
    return dict_of_answer


def get_answers(question_id):
    '''returns a dictionary of ditionaries containing all the answers with the given question_id'''
    DatabaseConnection._cursor.execute("SELECT * FROM answer WHERE question_id = %s;", [question_id])
    result_set = DatabaseConnection._cursor.fetchall()
    answers = construct_answer_dicts(result_set)
    return answers


def new_question(question):
    '''
    adds a new question to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, view_number::int, vote_number::int, title::str, message::str, image::str
    '''
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = "INSERT INTO question (submission_time, view_number, vote_number, title, message, image) \
             VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);"
    DatabaseConnection._cursor.execute(query, final_question)
    query = "SELECT id FROM question ORDER BY id DESC LIMIT 1;"
    DatabaseConnection._cursor.execute(query)
    return DatabaseConnection._cursor.fetchall()[0][0]


def new_answer(answer):
    '''
    adds a new answer to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, vote_number::int, question_id::int, message::str, image::str
    '''
    final_answer = dict(answer)
    final_answer['submission_time'] = datetime.datetime.fromtimestamp(final_answer['submission_time'])
    query = "INSERT INTO answer (submission_time, vote_number, question_id, message, image) \
             VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);"
    DatabaseConnection._cursor.execute(query, final_answer)


# TODO: we need to update the title and view_number too
def update_question(question):
    '''
    updates a question in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, view_number::int, vote_number::int, title::str, message::str, image::str
    '''
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = "UPDATE question \
             SET submission_time = %(submission_time)s, vote_number = %(vote_number)s, \
             message = %(message)s, image = %(image)s WHERE id = %(id)s"
    DatabaseConnection._cursor.execute(query, final_question)


def update_answer(answer):
    '''
    updates an answer in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, vote_number::int, message::str, image::str
    '''
    submitted_answer = dict(answer)
    submitted_answer['submission_time'] = datetime.datetime.fromtimestamp(submitted_answer['submission_time'])
    query = "UPDATE answer \
             SET submission_time = %(submission_time)s, vote_number = %(vote_number)s, \
             message = %(message)s, image = %(image)s WHERE id = %(id)s;"
    DatabaseConnection._cursor.execute(query, submitted_answer)


def delete_question(question_id):
    '''
    deletes a question from the database with the given id\n
    also deletes al the answers that are for that question
    '''
    query_answer = 'DELETE FROM answer WHERE question_id = %s;'
    DatabaseConnection._cursor.execute(query_answer, [question_id])
    query_question = 'DELETE FROM question WHERE id = %s;'
    DatabaseConnection._cursor.execute(query_question, [question_id])


def delete_answer(answer_id):
    '''deletes an answer from the database with the given id'''
    query = "DELETE FROM answer WHERE id = %s;"
    DatabaseConnection._cursor.execute(query, [answer_id])


def construct_question_dicts(result_set):
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing questions'''
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
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing answers'''
    answers = dict()
    for answer in result_set:
        answers[answer[0]] = {
            'id': answer[0],
            'submission_time': answer[1].timestamp(),
            'vote_number': answer[2],
            'question_id': answer[3],
            'message': answer[4],
            'image': answer[5]
        }
    return answers
