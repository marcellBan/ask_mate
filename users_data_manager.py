import datetime
import time

import psycopg2

from db_connect import connect_to_database


@connect_to_database
def username_exists(user_name):
    query = (
        '''SELECT user_name '''
        '''FROM users '''
        '''WHERE user_name = %s;''')
    _cursor.execute(query, [user_name])
    return True if _cursor.fetch() else False


@connect_to_database
def new_user(user_name, password):
    user_data = {
        'user_name': user_name,
        'password': password,
        'registration_time': int(time.time())
    }
    query = (
        '''INSERT INTO users '''
        '''     (user_name, password, registration_time) '''
        '''VALUES '''
        '''     (%(user_name)s, %(password)s, %(registration_time)s);'''
    )
    _cursor.execute(query, user_data)
