import os
import psycopg2
from flask import abort


def connect_to_database(func_to_be_connected):
    def connection(*args, **kwargs):
        _db_connection = None
        _cursor = None
        connection_data = {
            'dbname': os.environ.get('MY_PSQL_DBNAME'),
            'user': os.environ.get('MY_PSQL_USER'),
            'host': os.environ.get('MY_PSQL_HOST'),
            'password': os.environ.get('MY_PSQL_PASSWORD')
        }
        # if environment values are missing send the user to Error number 500 page
        if any(map(lambda x: x is None, connection_data.values())):
            abort(500, 'No database config found.')
        connect_string = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        connect_string = connect_string.format(**connection_data)
        try:
            _db_connection = psycopg2.connect(connect_string)
            _db_connection.autocommit = True
            _cursor = _db_connection.cursor()
            result = func_to_be_connected(*args, **kwargs, _cursor=_cursor)
            _cursor.close()
            _db_connection.close()
        except psycopg2.DatabaseError:
            abort(500, 'Couldn\'t connect to database.')
        return result
    return connection
