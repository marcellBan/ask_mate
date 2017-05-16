'''
data manager for AskMate
persists data in local csv files
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

_db_connection = None
_cursor = None


def connect_to_database():
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


def close_database_connection():
    if _cursor is not None:
        _cursor.close()
    if _db_connection is not None:
        _db_connection.close()


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
