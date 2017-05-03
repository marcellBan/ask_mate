'''
Display the questions from questions.csv file
For AskMate by SzószKód
'''

from data_manager import load_data
from flask import render_template


def display_questions():
    dict_list = load_data()
    list_dict = []
    for key, value in dict_list.items():
        new_dict = {}
        for element in value:
            new_dict[key] = element
        list_dict.append(new_dict)
    # data = [dict(zip(loaded_data, t)) for t in zip(*loaded_data.values())]
    return render_template('list.html', question_list=list_dict)


def display_one_question(q_id):
    question = load_data().get(q_id)
    answers = list(filter(lambda x: x.get('question_id') == q_id, load_data(answers=True).values()))
    answers.sort(key=lambda x: x.get('submission_time'), reverse=True)
    return render_template('question.html', question=question, answers=answers)
