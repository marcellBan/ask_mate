'''
data manager for AskMate
persists data in postgres database
by SzószKód
'''

import os
import datetime
import psycopg2


def connect_to_database(func_to_be_connected):
    def connection(*args, **kwargs):
        global _cursor
        _db_connection = None
        _cursor = None
        connection_data = {
            'dbname': os.environ.get('MY_PSQL_DBNAME'),
            'user': os.environ.get('MY_PSQL_USER'),
            'host': os.environ.get('MY_PSQL_HOST'),
            'password': os.environ.get('MY_PSQL_PASSWORD')
        }
        connect_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect_string = connect_string.format(**connection_data)
        _db_connection = psycopg2.connect(connect_string)
        _db_connection.autocommit = True
        _cursor = _db_connection.cursor()
        result = func_to_be_connected(*args, **kwargs)
        _cursor.close()
        _db_connection.close()
        return result
    return connection


@connect_to_database
def get_question(question_id):
    '''returns a dictionary containing all the information of a question with the given id'''
    _cursor.execute("SELECT * FROM question WHERE id = %s;", [question_id])
    question = _cursor.fetchall()[0]
    dict_of_question = {'id': question[0],
                        'submission_time': question[1].timestamp(),
                        'view_number': question[2],
                        'vote_number': question[3],
                        'title': question[4],
                        'message': question[5],
                        'image': question[6]}
    return dict_of_question


@connect_to_database
def get_questions(sorting=None, limit=None):
    '''
    returns a list of dictionaries containing all the questions\n
    the amount of questions returened can be limited with the limit parameter\n
    the sorting parameter is should be None or a list of tuples containing the column and the sorting order
    '''
    if sorting is None:
        sorting_query = "ORDER BY submission_time DESC"
    else:
        sorting_query = "ORDER BY {} {}".format(sorting[0][0], sorting[0][1].upper())
        if len(sorting) > 1:
            for item in sorting[1:]:
                sorting_query += ", {} {}".format(item[0], item[1].upper())
    limit_query = ""
    if limit is not None:
        limit_query = "LIMIT {}".format(limit)
    query = "SELECT * FROM question {} {};".format(sorting_query, limit_query)
    _cursor.execute(query)
    questions = _cursor.fetchall()
    questions = construct_question_list(questions)
    return questions


@connect_to_database
def get_answer(answer_id):
    '''returns a dictionary containing all the information of an answer with the given id'''
    _cursor.execute("SELECT * FROM answer WHERE id = %s;", [answer_id])
    answer = _cursor.fetchall()[0]
    dict_of_answer = {'id': answer[0],
                      'submission_time': answer[1].timestamp(),
                      'vote_number': answer[2],
                      'question_id': answer[3],
                      'message': answer[4],
                      'image': answer[5]}
    return dict_of_answer


@connect_to_database
def get_answers(question_id):
    '''returns a list of ditionaries containing all the answers with the given question_id'''
    _cursor.execute(
        "SELECT * FROM answer WHERE question_id = %s ORDER BY vote_number DESC, submission_time ASC;",
        [question_id]
    )
    result_set = _cursor.fetchall()
    answers = construct_answer_list(result_set)
    return answers


@connect_to_database
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
    _cursor.execute(query, final_question)
    query = "SELECT id FROM question ORDER BY id DESC LIMIT 1;"
    _cursor.execute(query)
    return _cursor.fetchall()[0][0]


@connect_to_database
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
    _cursor.execute(query, final_answer)


@connect_to_database
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
             message = %(message)s, image = %(image)s, \
             view_number = %(view_number)s, title = %(title)s \
             WHERE id = %(id)s;"
    _cursor.execute(query, final_question)


@connect_to_database
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
    _cursor.execute(query, submitted_answer)


@connect_to_database
def delete_question(question_id):
    '''
    deletes a question from the database with the given id\n
    also deletes al the answers that are for that question
    '''
    query_answer = 'DELETE FROM answer WHERE question_id = %s;'
    _cursor.execute(query_answer, [question_id])
    query_question = 'DELETE FROM question WHERE id = %s;'
    _cursor.execute(query_question, [question_id])


@connect_to_database
def delete_answer(answer_id):
    '''deletes an answer from the database with the given id'''
    query = "DELETE FROM answer WHERE id = %s;"
    _cursor.execute(query, [answer_id])


@connect_to_database
def delete_comment(comment_id):
    query = 'DELETE FROM comment WHERE id = %s;'
    _cursor.execute(query, [comment_id])


@connect_to_database
def get_comment(comment_id):
    query = "SELECT * FROM comment WHERE id = %s;"
    _cursor.execute(query, [comment_id])
    result_set = _cursor.fetchall()[0]
    comment = {
        'id': result_set[0],
        'question_id': result_set[1],
        'answer_id': result_set[2],
        'message': result_set[3],
        'submission_time': result_set[4].timestamp(),
        'edit_count': result_set[5]
    }
    return comment


def construct_question_list(result_set):
    '''constructs a list of dictionaries from an SQL Query result set (list of tuples) representing questions'''
    questions = list()
    for question in result_set:
        questions.append({
            'id': question[0],
            'submission_time': question[1].timestamp(),
            'view_number': question[2],
            'vote_number': question[3],
            'title': question[4],
            'message': question[5],
            'image': question[6]
        })
    return questions


def construct_answer_list(result_set):
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing answers'''
    answers = list()
    for answer in result_set:
        answers.append({
            'id': answer[0],
            'submission_time': answer[1].timestamp(),
            'vote_number': answer[2],
            'question_id': answer[3],
            'message': answer[4],
            'image': answer[5]
        })
    return answers


@connect_to_database
def new_comment(comment):
    '''
    adds a new comment to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, message::str, question_id::int, answer_id::None
    '''
    final_comment = dict(comment)
    final_comment['submission_time'] = datetime.datetime.fromtimestamp(final_comment['submission_time'])
    query = "INSERT INTO comment (submission_time, message, question_id, answer_id, edit_count) \
             VALUES (%(submission_time)s, %(message)s, %(question_id)s, %(answer_id)s, %(edit_count)s);"
    _cursor.execute(query, final_comment)


@connect_to_database
def get_comments_for_question(question_id):
    '''returns a dictionary of ditionaries containing all the comments with the given question_id'''
    _cursor.execute(
        "SELECT * FROM comment WHERE question_id = %s ORDER BY submission_time ASC;",
        [question_id]
    )
    result_set = _cursor.fetchall()
    comments = construct_comment_list(result_set)
    return comments


@connect_to_database
def get_comments_for_answer(answer_id):
    '''returns a dictionary of dictionaries containing all the comments with the given answer_id'''
    _cursor.execute(
        "SELECT * FROM comment WHERE answer_id = %s ORDER BY submission_time ASC;",
        [answer_id]
    )
    result_set = _cursor.fetchall()
    comments = construct_comment_list(result_set)
    return comments


def construct_comment_list(result_set):
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing comments'''
    comments = list()
    for comment in result_set:
        comments.append({
            'id': comment[0],
            'question_id': comment[1],
            'answer_id': comment[2],
            'message': comment[3],
            'submission_time': comment[4].timestamp(),
            'edit_count': comment[5]
        })
    return comments


@connect_to_database
def update_comment(comment):
    '''
    updates a comment in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, message::str, edit_count::int
    '''
    submitted_comment = dict(comment)
    submitted_comment['submission_time'] = datetime.datetime.fromtimestamp(submitted_comment['submission_time'])
    query = "UPDATE comment \
             SET submission_time = %(submission_time)s, edit_count = %(edit_count)s, \
             message = %(message)s WHERE id = %(id)s;"
    _cursor.execute(query, submitted_comment)
