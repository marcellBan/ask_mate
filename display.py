'''
Display the questions from questions.csv file
For AskMate by SzószKód
'''

from data_manager import load_data, save_data
from flask import render_template, redirect, request


def display_questions():
    list_dict = list(load_data().values())
    list_dict.sort(key=lambda x: x.get("submission_time"), reverse=True)
    loaded_answers = list(load_data(answers=True).values())
    for dictionary in list_dict:
        counter = 0
        for answer in loaded_answers:
            if answer['question_id'] == dictionary['id']:
                counter += 1
        dictionary['answer_count'] = counter
    return render_template('list.html', question_list=list_dict)


def display_one_question(q_id):
    questions = load_data()
    questions[q_id]['view_number'] += 1
    question = dict(questions.get(q_id))
    save_data(questions)
    answers = list(filter(lambda x: x.get('question_id') == q_id, load_data(answers=True).values()))
    answers.sort(key=lambda x: x.get('submission_time'), reverse=True)
    question['answer_count'] = len(answers)
    return render_template('question.html', question=question, answers=answers)


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
        questions = list(load_data().values())
        loaded_answers = load_data(answers=True)
        if skey != 'title':
            questions.sort(key=lambda x: x.get(skey), reverse=rev)
        else:
            questions.sort(key=lambda x: x.get(skey).lower(), reverse=rev)
        for question in questions:
            counter = 0
            for answer in loaded_answers.values():
                if answer['question_id'] == question['id']:
                    counter += 1
            question['answer_count'] = counter
        return render_template('list.html', question_list=questions)
