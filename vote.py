'''Vote module for AskMate
by SzószKód
'''
from flask import flash, redirect, request, url_for

import data_manager


def downvote_question(question_id):
    question = data_manager.get_question(question_id)
    question['vote_number'] -= 1
    data_manager.update_question(question)
    flash('Successfully downvoted this question!')
    if request.args.get('next') is not None:
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('index'))


def upvote_question(question_id):
    question = data_manager.get_question(question_id)
    question['vote_number'] += 1
    data_manager.update_question(question)
    flash('Successfully upvoted this question!')
    if request.args.get('next') is not None:
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return redirect(url_for('index'))


def downvote_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    answer['vote_number'] -= 1
    data_manager.update_answer(answer)
    flash('Successfully downvoted the answer: ({})'.format(answer_id))
    return redirect(url_for('display_question', question_id=answer['question_id']))


def upvote_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    answer['vote_number'] += 1
    data_manager.update_answer(answer)
    flash('Successfully upvoted the answer ({})'.format(answer_id))
    return redirect(url_for('display_question', question_id=answer['question_id']))
