'''Vote module for AskMate
by SzószKód
'''
from flask import flash, redirect, request, url_for

import data_manager


def downvote_question(q_id):
    questions = data_manager.load_data()
    questions[q_id]['vote_number'] -= 1
    data_manager.save_data(questions)
    flash('Successfully downvoted a question :(')
    return redirect(url_for('index'))


def upvote_question(q_id):
    questions = data_manager.load_data()
    questions[q_id]['vote_number'] += 1
    data_manager.save_data(questions)
    flash('Successfully upvoted a question!')
    return redirect(url_for('index'))


def downvote_answer(a_id):
    answers = data_manager.load_data(answers=True)
    answers[a_id]['vote_number'] -= 1
    flash('Successfully downvoted an answer :(')
    return redirect(url_for('display_question', q_id=answers[a_id]['question_id']))


def upvote_answer(a_id):
    answers = data_manager.load_data(answers=True)
    answers[a_id]['vote_number'] += 1
    flash('Successfully upvoted an answer!')
    return redirect(url_for('display_question', q_id=answers[a_id]['question_id']))
