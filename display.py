'''
Display the questions from the database
For AskMate by SzószKód
'''

import data_manager
from flask import render_template, redirect, request, session, url_for


def display_questions():
    questions_list = data_manager.get_questions()
    for question in questions_list:
        question['answer_count'] = len(data_manager.get_answers(question['id']))
    return render_template('list.html', question_list=questions_list, page='')


def display_one_question(question_id):
    question = data_manager.get_question(question_id)
    question['view_number'] += 1
    data_manager.update_question(question)
    answers = data_manager.get_answers(question_id)
    for answer in answers:
        answer['comments'] = data_manager.get_comments_for_answer(answer['id'])
    question['answer_count'] = len(answers)
    question['comments'] = data_manager.get_comments_for_question(question_id)
    return render_template('question.html', question=question, answers=answers)


def display_five_latest_questions():
    questions_list = data_manager.get_questions(limit=5)
    for question in questions_list:
        question['answer_count'] = len(data_manager.get_answers(question['id']))
    return render_template('list.html', question_list=questions_list, page='index')


def display_sorted_questions():
    aspect_list = (
        'id',
        'submission_time',
        'title',
        'view_number',
        'vote_number'
    )
    if session.get('sorting') is None:
        session['sorting'] = list()
    for aspect in aspect_list:
        if request.args.get(aspect) is not None:
            flag = False
            for sort in session['sorting']:
                if sort[0] == aspect:
                    sort[1] = request.args.get(aspect)
                    flag = True
            if not flag:
                session['sorting'].append([aspect, request.args.get(aspect)])
    questions = data_manager.get_questions(sorting=session['sorting'])
    for question in questions:
        question['answer_count'] = len(data_manager.get_answers(question['id']))
    return render_template('list.html', question_list=questions, page='sorted')


def clear_sorting():
    if session.get('sorting') is not None:
        del(session['sorting'])
    return redirect(url_for('list_index'))


def list_users():
    return render_template('list_users.html')
