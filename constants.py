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
