import os
import psycopg2


def connect_to_database(func_to_be_connected):
    def connection(*args, **kwargs):
        nonlocal _cursor
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
