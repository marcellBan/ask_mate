import psycopg2
import datetime
from db_connect import connect_to_database


@connect_to_database
def delete_comment(comment_id, _cursor=None):
    query = '''DELETE FROM comment
                 WHERE id = %s;'''
    _cursor.execute(query, [comment_id])


@connect_to_database
def get_comment(comment_id, _cursor=None):
    query = '''SELECT *
                 FROM comment
                 WHERE id = %s;'''
    _cursor.execute(query, [comment_id])
    if _cursor.rowcount == 0:
        raise ValueError
    comment = _cursor.fetchall()[0]
    comment = {'id': comment[0],
               'question_id': comment[1],
               'answer_id': comment[2],
               'user_name': comment[3],
               'message': comment[4],
               'submission_time': comment[5].timestamp(),
               'edit_count': comment[6]}
    return comment


@connect_to_database
def new_comment(comment, _cursor=None):
    '''
    adds a new comment to the database\n
    the parameter should be a dictionary with the following keys:\n
    submission_time::timestamp, message::str, question_id::int, answer_id::int, user_name::str
    '''
    final_comment = dict(comment)
    final_comment['submission_time'] = datetime.datetime.fromtimestamp(final_comment['submission_time'])
    query = '''INSERT INTO comment (submission_time, message, question_id, answer_id, edit_count, user_name)
                 VALUES
                 (%(submission_time)s, %(message)s, %(question_id)s, %(answer_id)s, %(edit_count)s, %(user_name)s);'''
    _cursor.execute(query, final_comment)


@connect_to_database
def get_comments_for_question(question_id, _cursor=None):
    '''returns a dictionary of ditionaries containing all the comments with the given question_id'''
    query = '''SELECT *
                 FROM comment
                 WHERE question_id = %s
                 ORDER BY submission_time ASC;'''
    _cursor.execute(query, [question_id])
    result_set = _cursor.fetchall()
    comments = construct_comment_list(result_set)
    return comments


@connect_to_database
def get_comments_for_answer(answer_id, _cursor=None):
    '''returns a dictionary of dictionaries containing all the comments with the given answer_id'''
    query = '''SELECT *
                 FROM comment
                 WHERE answer_id = %s
                 ORDER BY submission_time ASC;'''
    _cursor.execute(query, [answer_id])
    result_set = _cursor.fetchall()
    comments = construct_comment_list(result_set)
    return comments


def construct_comment_list(result_set):
    '''constructs a dictionary of dictionaries from an SQL Query result set (list of tuples) representing comments'''
    comments = list()
    for comment in result_set:
        comments.append({'id': comment[0],
                         'question_id': comment[1],
                         'answer_id': comment[2],
                         'user_name': comment[3],
                         'message': comment[4],
                         'submission_time': comment[5].timestamp(),
                         'edit_count': comment[6]})
    return comments


@connect_to_database
def update_comment(commen, _cursor=None):
    '''
    updates a comment in the database
    the parameter should be a dictionary with the following keys:\n
    id::int, submission_time::timestamp, message::str, edit_count::int
    '''
    submitted_comment = dict(comment)
    submitted_comment['submission_time'] = datetime.datetime.fromtimestamp(submitted_comment['submission_time'])
    query = '''UPDATE comment
                 SET submission_time = %(submission_time)s, edit_count = %(edit_count)s,
                 message = %(message)s WHERE id = %(id)s;'''
    _cursor.execute(query, submitted_comment)
