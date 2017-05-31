import datetime
import psycopg2
from db_connect import connect_to_database


@connect_to_database
def get_question(question_id, _cursor=None):
    '''returns a dictionary containing all the information of a question with the given id'''
    query = '''SELECT *
                 FROM question
                 WHERE id = %s;'''
    _cursor.execute(query, [question_id])
    question = _cursor.fetchall()[0]
    dict_of_question = {'id': question[0],
                        'user_name': question[1],
                        'submission_time': question[2].timestamp(),
                        'view_number': question[3],
                        'vote_number': question[4],
                        'title': question[5],
                        'message': question[6],
                        'image': question[7],
                        'has_accepted_answer': question[8]}
    return dict_of_question


@connect_to_database
def get_questions(sorting=None, limit=None, _cursor=None):
    '''
    returns a list of dictionaries containing all the questions\n
    the amount of questions returened can be limited with the limit parameter\n
    the sorting parameter is should be None or a list of lists containing the column and the sorting order
    '''
    order_by_clause = get_order_by_clause(sorting)
    limit_clause = get_limit_clause(limit)
    query = '''SELECT *
                 FROM question
                 {} {};'''
    query = query.format(order_by_clause, limit_clause)
    _cursor.execute(query)
    questions = _cursor.fetchall()
    questions = construct_question_list(questions)
    return questions


def get_order_by_clause(sorting):
    if sorting is None:
        order_by_clause = "ORDER BY submission_time DESC"
    else:
        order_by_clause = "ORDER BY {} {}".format(sorting[0][0], sorting[0][1].upper())
        if len(sorting) > 1:
            for item in sorting[1:]:
                order_by_clause += ", {} {}".format(item[0], item[1].upper())
    return order_by_clause


def get_limit_clause(limit):
    limit_clause = ""
    if limit is not None:
        limit_clause = "LIMIT {}".format(limit)
    return limit_clause


@connect_to_database
def new_question(question, _cursor=None):
    '''
    adds a new question to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, view_number::int, vote_number::int,
    title::str, message::str, image::str, user_name::str
    '''
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = '''INSERT INTO question (submission_time, view_number, vote_number,
                 title, message, image, user_name)
                 VALUES
                   (%(submission_time)s, %(view_number)s, %(vote_number)s,
                   %(title)s, %(message)s, %(image)s, %(user_name)s);'''
    _cursor.execute(query, final_question)
    query = '''SELECT id
                 FROM question
                 ORDER BY id DESC
                 LIMIT 1;'''
    _cursor.execute(query)
    return _cursor.fetchall()[0][0]


@connect_to_database
def update_question(question, _cursor=None):
    '''
    updates a question in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, view_number::int, vote_number::int, title::str, message::str, image::str
    '''
    final_question = dict(question)
    final_question['submission_time'] = datetime.datetime.fromtimestamp(final_question['submission_time'])
    query = '''UPDATE question
                 SET submission_time = %(submission_time)s, vote_number = %(vote_number)s,
                   message = %(message)s, image = %(image)s,
                   view_number = %(view_number)s, title = %(title)s
                 WHERE id = %(id)s;'''
    _cursor.execute(query, final_question)


@connect_to_database
def delete_question(question_id, _cursor=None):
    '''
    deletes a question from the database with the given id\n
    also deletes al the answers that are for that question
    '''
    query = '''DELETE FROM comment
                 WHERE answer_id IN
                   (SELECT id
                      FROM answer
                      WHERE question_id = %(question_id)s)
                   OR question_id = %(question_id)s;
               DELETE FROM answer
                 WHERE question_id = %(question_id)s;
               DELETE FROM question
                 WHERE id = %(question_id)s;'''
    _cursor.execute(query, {'question_id': question_id})


def construct_question_list(result_set):
    '''constructs a list of dictionaries from an SQL Query result set (list of tuples) representing questions'''
    questions = list()
    for question in result_set:
        questions.append({'id': question[0],
                          'submission_time': question[1].timestamp(),
                          'view_number': question[2],
                          'vote_number': question[3],
                          'title': question[4],
                          'message': question[5],
                          'image': question[6],
                          'has_accepted_answer': question[7],
                          'user_id': question[8],
                          'user_name': question[9]})
    return questions
