'''
entry manager module for AskMate
by SzószKód
'''

from flask import render_template, redirect, request, url_for, flash
import data_manager
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
            question = {
                'submission_time': int(time.time()),
                'view_number': 0,
                'vote_number': 0,
                'title': request.form.get('title'),
                'message': request.form.get('message'),
                'image': request.files.get('image').filename
            }
            q_id = data_manager.new_question(question)
            return redirect(url_for('display_question', q_id=q_id))


def delete_question(q_id):
    data_manager.delete_question(q_id)
    return redirect(url_for('index'))


def edit_question(q_id):
    question = data_manager.get_question(q_id)
    form_title = question['title']
    form_message = question['message']
    if request.method == 'GET':
        return render_template('new_question.html', form_title=form_title, form_message=form_message)
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your question isn\'t long enough!')
            return render_template(
                'new_question.html',
                form_title=request.form.get('title'), form_message=request.form.get('message'))
        else:
            question['title'] = request.form.get('title')
            question['message'] = request.form.get('message')
            question['submission_time'] = int(time.time())
            data_manager.update_question(question)
            return redirect(url_for('display_question', q_id=q_id))


def add_answer(q_id):
    question = data_manager.get_question(q_id)
    if request.method == 'GET':
        return render_template('new_answer.html', question=question)
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your answer isn\'t long enough!')
            return render_template(
                'new_answer.html', question=question, form_message=request.form.get('message')
            )
        else:
            answer = {
                'submission_time': int(time.time()),
                'vote_number': 0,
                'question_id': q_id,
                'message': request.form.get('message'),
                'image': request.files.get('image').filename
            }
            data_manager.new_answer(answer)
            return redirect(url_for('display_question', q_id=q_id))


def delete_answer(a_id):
    q_id = data_manager.get_answer(a_id).get('question_id')
    data_manager.delete_answer(a_id)
    return redirect(url_for('display_question', q_id=q_id))


def edit_answer(a_id):
    answer = data_manager.get_answer(a_id)
    q_id = answer.get('question_id')
    question = data_manager.get_question(q_id)
    if request.method == 'GET':
        return render_template('new_answer.html', question=question, form_message=answer.get('message'))
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your answer isn\'t long enough!')
            return render_template(
                'new_answer.html', question=question, form_message=request.form.get('message')
            )
        else:
            answer['submission_time'] = int(time.time())
            answer['message'] = request.form.get('message')
            answer['image'] = request.files.get('image').filename
            data_manager.update_answer(answer)
            return redirect(url_for('display_question', q_id=q_id))
