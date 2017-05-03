'''
Display the questions from questions.csv file
For AskMate by SzószKód
'''

from data_manager import load_data
from flask import render_template


def display_questions():
    data = load_data()
    return render_template('.html')


def display_one_question(q_id):
    question = load_data().get(q_id)
    answers = list(filter(lambda x: x.get('question_id') == q_id, load_data(answers=True).values()))
    answers.sort(key=lambda x: x.get('submission_time'), reverse=True)
    return render_template('question.html', question=question, answers=answers)
