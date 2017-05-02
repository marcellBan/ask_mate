'''
data manager for AskMate
persists data in local csv file
by SzószKód
'''

import csv
import os
from constants import QUESTIONS_FILE, ANSWERS_FILE, QUESTION_FIELDS, ANSWER_FIELDS


def load_data(answers=False):
    '''returns a dict of dicts containing the current data in the database'''
    data = dict()
    filepath = ANSWERS_FILE if answers else QUESTIONS_FILE
    fields = ANSWER_FIELDS if answers else QUESTION_FIELDS
    if os.path.isfile(filepath):
        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fields,
                                    delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)
            for row in reader:
                row['id'] = int(row['id'])
                data[row['id']] = row
    return data


def save_data(data, answers=False):
    '''saves a dict of dicts to the database'''
    filepath = ANSWERS_FILE if answers else QUESTIONS_FILE
    fields = ANSWER_FIELDS if answers else QUESTION_FIELDS
    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, delimiter=';', quotechar='|', quoting=csv.QUOTE_ALL)
        for row in data:
            writer.writerow(data[row])