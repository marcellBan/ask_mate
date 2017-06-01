from flask import render_template, redirect, request, url_for, flash, session
import question_data_manager
import answer_data_manager
import time


def add_answer(question_id):
    question = question_data_manager.get_question(question_id)
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
                'image': request.files.get('image').filename,
                'user_name': session.get('user_name')
            }
            answer_data_manager.new_answer(answer)
            return redirect(url_for('display_question', question_id=question_id))


def edit_answer(answer_id):
    answer = answer_data_manager.get_answer(answer_id)
    question_id = answer.get('question_id')
    question = question_data_manager.get_question(question_id)
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
            answer_data_manager.update_answer(answer)
            return redirect(url_for('display_question', question_id=question_id))


def delete_answer(answer_id):
    question_id = answer_data_manager.get_answer(answer_id).get('question_id')
    answer_data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=question_id))


def accepted_answer(answer_id):
    session['prev'] = request.url
    answer = answer_data_manager.get_answer(answer_id)
    question = question_data_manager.get_question(answer['question_id'])
    question_id = question['question_id']
    if session['user_name'] != question['user_name']:
        flash('This is not your question!')
        return redirect(session['prev'])
    else:
        if answer['accepted_answer'] is True:
            flash('There is already an accepted answer!')
            return redirect(session['prev'])
        elif answer['accepted_answer'] is False:
            answer['accepted_answer'] = True
            question['has_accepted_answer'] = True
            answer_data_manager.update_answer(answer)
            question_data_manager.update_question(question)
            return redirect(url_for('display_question', question_id=question_id, answer_id=answer_id))
