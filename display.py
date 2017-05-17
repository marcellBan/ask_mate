'''
Display the questions from the database
For AskMate by SzószKód
'''

import data_manager
from flask import render_template, redirect, request


def display_questions():
    questions_list = list(data_manager.get_questions().values())
    questions_list.sort(key=lambda x: x.get("submission_time"), reverse=True)
    loaded_answers = list(data_manager.get_answers().values())
    for question in questions_list:
        question['answer_count'] = len(data_manager.get_answers(question['id']))
    return render_template('list.html', question_list=questions_list)


def display_one_question(q_id):
    question = data_manager.get_question(q_id)
    question['view_number'] += 1
    data_manager.update_question(question)
    answers = data_manager.get_answers(q_id)
    answers.sort(key=lambda x: x.get('submission_time'), reverse=True)
    question['answer_count'] = len(answers)
    return render_template('question.html', question=question, answers=answers)


# TODO: this needs total refactoring to data_manager
def display_sorted_questions():
    skey = None
    rev = False
    if request.args.get('id') is not None:
        skey = 'id'
        if request.args.get('id') == 'desc':
            rev = True
        elif request.args.get('id') != 'asc':
            skey = None
    elif request.args.get('time') is not None:
        skey = 'submission_time'
        if request.args.get('time') == 'desc':
            rev = True
        elif request.args.get('time') != 'asc':
            skey = None
    elif request.args.get('title') is not None:
        skey = 'title'
        if request.args.get('title') == 'desc':
            rev = True
        elif request.args.get('title') != 'asc':
            skey = None
    elif request.args.get('views') is not None:
        skey = 'view_number'
        if request.args.get('views') == 'desc':
            rev = True
        elif request.args.get('views') != 'asc':
            skey = None
    elif request.args.get('rating') is not None:
        skey = 'vote_number'
        if request.args.get('rating') == 'desc':
            rev = True
        elif request.args.get('rating') != 'asc':
            skey = None

    if skey is None:
        return redirect(url_for('index'))
    else:
        questions = list(data_manager.get_questions().values())
        loaded_answers = data_manager.get_answers()
        if skey != 'title':
            questions.sort(key=lambda x: x.get(skey), reverse=rev)
        else:
            questions.sort(key=lambda x: x.get(skey).lower(), reverse=rev)
        for question in questions:
            question['answer_count'] = len(data_manager.get_answers(question['id']))
        return render_template('list.html', question_list=questions)
