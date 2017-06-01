from flask import render_template, redirect, request, url_for, flash, session
import comment_data_manager
import question_data_manager
import answer_data_manager
import time


def new_comment_for_question(question_id):
    question = question_data_manager.get_question(question_id)
    if request.method == 'GET':
        session['prev'] = request.url
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
                'submission_time': int(time.time()),
                'edit_count': 0,
                'user_name': session.get('user_name')
            }
            comment_data_manager.new_comment(comment)
            return redirect(
                url_for('display_question', question_id=question_id)
            )


def new_comment_for_answer(answer_id):
    answer = answer_data_manager.get_answer(answer_id)
    if request.method == 'GET':
        session['prev'] = request.url
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
                'submission_time': int(time.time()),
                'edit_count': 0,
                'user_name': session.get('user_name')
            }
            comment_data_manager.new_comment(comment)
            return redirect(
                url_for('display_question', question_id=answer.get('question_id'))
            )


def edit_comment(comment_id):
    comment = comment_data_manager.get_comment(comment_id)
    question_id = get_question_id(comment_id)
    if comment['answer_id'] is None:
        session['prev'] = request.url
        entry = question_data_manager.get_question(comment['question_id'])
    else:
        entry = answer_data_manager.get_answer(comment['answer_id'])
    if request.method == 'GET':
        return render_template('new_comment.html', entry=entry, form_message=comment.get('message'))
    elif request.method == 'POST':
        if len(request.form.get('message')) < 10:
                flash('Your comment isn\'t long enough!')
                return render_template(
                    'new_comment.html', entry=entry, form_message=request.form.get('message')
                )
        else:
            comment['submission_time'] = int(time.time())
            comment['message'] = request.form.get('message')
            comment['edit_count'] += 1
            comment_data_manager.update_comment(comment)
            return redirect(url_for('display_question', question_id=question_id))


def delete_comment(comment_id):
    question_id = get_question_id(comment_id)
    comment_data_manager.delete_comment(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


def get_question_id(comment_id):
    comment = comment_data_manager.get_comment(comment_id)
    if comment['answer_id'] is None:
        return comment['question_id']
    else:
        answer = answer_data_manager.get_answer(comment['answer_id'])
        return answer['question_id']
