'''
constants used in AskMate
by SzószKód
'''

QUESTIONS_FILE = 'data/question.csv'
ANSWERS_FILE = 'data/answer.csv'
QUESTION_FIELDS = (
    'id',
    'submission_time',
    'view_number',
    'vote_number',
    'title',
    'message',
    'image'
)
ANSWER_FIELDS = (
    'id',
    'submission_time',
    'vote_number',
    'question_id',
    'message',
    'image'
)
ENCODE_QUESTION_FIELDS = (
    'title',
    'message',
    'image'
)
ENCODE_ANSWER_FIELDS = (
    'message',
    'image'
)
CONVERT_QUESTION_FIELDS = (
    ('submission_time', int),
    ('view_number', int),
    ('vote_number', int)
)
CONVERT_ANSWER_FIELDS = (
    ('submission_time', int),
    ('vote_number', int),
    ('question_id', int)
)
