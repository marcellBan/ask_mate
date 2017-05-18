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
            question_id = data_manager.new_question(question)
            return redirect(url_for('display_question', question_id=question_id))


def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('index'))


def edit_question(question_id):
    question = data_manager.get_question(question_id)
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
            return redirect(url_for('display_question', question_id=question_id))


def add_answer(question_id):
    question = data_manager.get_question(question_id)
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
                'question_id': question_id,
                'message': request.form.get('message'),
                'image': request.files.get('image').filename
            }
            data_manager.new_answer(answer)
            return redirect(url_for('display_question', question_id=question_id))


def delete_answer(answer_id):
    question_id = data_manager.get_answer(answer_id).get('question_id')
    data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


def edit_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    question_id = answer.get('question_id')
    question = data_manager.get_question(question_id)
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
            return redirect(url_for('display_question', question_id=question_id))


def new_comment_for_question(question_id):
    question = data_manager.get_question(question_id)
    if request.method == 'GET':
        return render_template('new_comment.html', entry=question)
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
                flash('Your comment isn\'t long enough!')
                return render_template(
                    'new_comment.html', entry=question, form_message=request.form.get('message')
                )
        else:
            comment = {
                'question_id': question_id,
                'answer_id': None,
                'message': request.form.get('message'),
                'submission_time': int(time.time())
            }
            data_manager.new_comment(comment)
            return redirect(
                url_for('display_question', question_id=question_id)
            )


def delete_comment(comment_id):
    question_id = data_manager.get_question_id_of_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


def new_comment_for_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    if request.method == 'GET':
        return render_template('new_comment.html', entry=answer)
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
            flash('Your comment isn\'t long enough!')
            render_template(
                'new_comment.html', entry=answer, form_message=request.form.get('message')
            )
        else:
            comment = {
                'question_id': None,
                'answer_id': answer_id,
                'message': request.form.get('message'),
                'submission_time': int(time.time())
            }
            data_manager.new_comment(comment)
            return redirect(
                url_for('display_question', question_id=answer.get('question_id'))
            )
