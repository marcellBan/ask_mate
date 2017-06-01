from flask import render_template, redirect, request, url_for, flash, session
import question_data_manager
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
                'image': request.files.get('image').filename,
                'user_name': session.get('user_name')
            }
            question_id = question_data_manager.new_question(question)
            return redirect(url_for('display_question', question_id=question_id))


def edit_question(question_id):
    question = question_data_manager.get_question(question_id)
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
            question_data_manager.update_question(question)
            return redirect(url_for('display_question', question_id=question_id))


def delete_question(question_id):
    question_data_manager.delete_question(question_id)
    return redirect(url_for('index'))
