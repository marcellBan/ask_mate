import datetime
import psycopg2
from db_connect import connect_to_database


@connect_to_database
def get_answer(answer_id, _cursor=None):
    '''returns a dictionary containing all the information of an answer with the given id'''
    query = '''SELECT *
                 FROM answer
                 WHERE id = %s;'''
    _cursor.execute(query, [answer_id])
    if _cursor.rowcount == 0:
        raise ValueError
    answer = _cursor.fetchall()[0]
    dict_of_answer = {'id': answer[0],
                      'question_id': answer[1],
                      'user_name': answer[2],
                      'submission_time': answer[3].timestamp(),
                      'vote_number': answer[4],
                      'message': answer[5],
                      'image': answer[6],
                      'accepted_answer': answer[7]}
    return dict_of_answer


@connect_to_database
def get_answers(question_id, _cursor=None):
    '''returns a list of ditionaries containing all the answers with the given question_id'''
    query = '''SELECT *
                 FROM answer
                 WHERE question_id = %s
                 ORDER BY
                   vote_number DESC,
                   submission_time ASC;'''
    _cursor.execute(query, [question_id])
    result_set = _cursor.fetchall()
    answers = construct_answer_list(result_set)
    return answers


@connect_to_database
def new_answer(answer, _cursor=None):
    '''
    adds a new answer to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, vote_number::int, question_id::int, message::str, image::str, user_name::str
    '''
    final_answer = dict(answer)
    final_answer['submission_time'] = datetime.datetime.fromtimestamp(final_answer['submission_time'])
    query = '''INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_name)
               VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_name)s);'''
    _cursor.execute(query, final_answer)


@connect_to_database
def update_answer(answer, _cursor=None):
    '''
    updates an answer in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, vote_number::int, message::str, image::str, accepted_answer::boolean
    '''
    submitted_answer = dict(answer)
    submitted_answer['submission_time'] = datetime.datetime.fromtimestamp(submitted_answer['submission_time'])
    query = '''UPDATE answer
                 SET submission_time = %(submission_time)s, vote_number = %(vote_number)s,
                 message = %(message)s, image = %(image)s, accepted_answer = %(accepted_answer)s WHERE id = %(id)s;'''
    _cursor.execute(query, submitted_answer)


@connect_to_database
def delete_answer(answer_id, _cursor=None):
    '''deletes an answer from the database with the given id'''
    query = '''DELETE FROM comment
                 WHERE answer_id = %(answer_id)s;
               DELETE FROM answer
                 WHERE id = %(answer_id)s;'''
    _cursor.execute(query, {'answer_id': answer_id})


def construct_answer_list(result_set):
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing answers'''
    answers = list()
    for answer in result_set:
        answers.append({'id': answer[0],
                        'question_id': answer[1],
                        'user_name': answer[2],
                        'submission_time': answer[3].timestamp(),
                        'vote_number': answer[4],
                        'message': answer[5],
                        'image': answer[6],
                        'accepted_answer': answer[7]})
    return answers
