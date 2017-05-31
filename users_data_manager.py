import datetime

import psycopg2

from db_connect import connect_to_database


@connect_to_database
def username_exists(user_name, _cursor=None):
    query = (
        '''SELECT user_name '''
        '''FROM users '''
        '''WHERE user_name = %s;''')
    _cursor.execute(query, [user_name])
    return True if _cursor.fetchone() else False


@connect_to_database
def new_user(user_data, _cursor=None):
    final_user_data = dict(user_data)
    final_user_data['registration_date'] = datetime.datetime.fromtimestamp(user_data['registration_date'])
    query = (
        '''INSERT INTO users '''
        '''     (user_name, password, registration_date) '''
        '''VALUES '''
        '''     (%(user_name)s, %(password)s, %(registration_date)s);'''
    )
    _cursor.execute(query, final_user_data)


@connect_to_database
def correct_credentials(user_data, _cursor=None):
    final_user_data = dict(user_data)
    query = '''SELECT user_name, password
                FROM users
                WHERE user_name = %(user_name)s;'''
    _cursor.execute(query, final_user_data)
    result = _cursor.fetchone()
    if not result:
        return False
    elif user_data['user_name'] != result[0] or user_data['password'] != result[1]:
        return False
    return True
