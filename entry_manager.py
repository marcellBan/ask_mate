'''
entry manager module for AskMate
by SzószKód
'''

from flask import render_template, redirect, request, url_for, flash
from data_manager import load_data, save_data
import time


def add_question():
    if request.method == 'GET':
        return render_template('new_question.html')
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your question isn\'t long enough!')
            return render_template(
                'new_question.html',
                form_title=request.form.get('title'), form_message=request.form.get('message')
            )
        else:
            data = load_data()
            maxid = -1 if len(data) == 0 else max(data.keys())
            data[maxid + 1] = {
                'id': maxid + 1,
                'submission_time': int(time.time()),
                'view_number': 0,
                'vote_number': 0,
                'title': request.form.get('title'),
                'message': request.form.get('message'),
                'image': request.form.get('image')
            }
            save_data(data)
            return redirect(url_for('display_question', q_id=maxid + 1))


def delete_question(q_id):
    question = load_data()
    answers = load_data(answers=True)
    del question[q_id]
    for row in answers:
        if answers[row]['question_id'] == q_id:
            del answers[row]
    save_data(question)
    save_data(answers, answers=True)
    return redirect(url_for('index'))


def edit_question():
    questions = load_data()
    form_title = 'placeholder 1'
    form_message = 'placeholder 2'

    if request.method == 'GET':
        return render_template('new_question.html')
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your question isn\'t long enough!')
            return render_template(
                'new_question.html',
                form_title=form_title, form_message=form_message
            )


def add_answer(q_id):
    question = load_data().get(q_id)
    if request.method == 'GET':
        return render_template('new_answer.html', question=question)
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your answer isn\'t long enough!')
            return render_template(
                'new_answer.html', question=question, form_message=request.form.get('message')
            )
        else:
            answers = load_data(answers=True)
            maxid = -1 if len(answers) == 0 else max(answers.keys())
            answers[maxid + 1] = {
                'id': maxid + 1,
                'submission_time': int(time.time()),
                'vote_number': 0,
                'question_id': q_id,
                'message': request.form.get('message'),
                'image': request.form.get('image')
            }
            save_data(answers, answers=True)
            return redirect(url_for('display_question', q_id=q_id))



def delete_answer(a_id):
    imported_data = load_data(answers=True)
    q_id = imported_data[a_id].get('question_id')
    del imported_data[a_id]
    save_data(imported_data, answers=True)
    return redirect(url_for('display_question', q_id=q_id))

