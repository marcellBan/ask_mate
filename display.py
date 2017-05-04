'''
Display the questions from questions.csv file
For AskMate by SzószKód
'''

from data_manager import load_data, save_data
from flask import render_template


def display_questions():
    list_dict = list(load_data().values())
    list_dict.sort(key=lambda x: x.get("submission_time"), reverse=True)
    loaded_answers = list(load_data(answers=True).values())
    for dictionary in list_dict:
        counter = 0
        for element in loaded_answers:
            if element['question_id'] == dictionary['id']:
                counter += 1
        dictionary['answer_count'] = counter
    return render_template('list.html', question_list=list_dict)


def display_one_question(q_id):
    questions = load_data()
    question = questions.get(q_id)
    question['view_number'] += 1
    save_data(questions)
    answers = list(filter(lambda x: x.get('question_id') == q_id, load_data(answers=True).values()))
    answers.sort(key=lambda x: x.get('submission_time'), reverse=True)
    return render_template('question.html', question=question, answers=answers)


def display_sorted_questions():
    skey = None
    if skey is None:
        return redirect(url_for('index'))
