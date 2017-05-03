'''Vote module for AskMate
by SzószKód
'''
from flask import flash, redirect, url_for


def downvote_question():
    flash("Redirected from downvote_question()")
    return redirect(url_for('index'))


def upvote_question():
    flash("Redirected from upvote_question()")
    return redirect(url_for('index'))


def downvote_answer():
    flash("Redirected from downvote_answer()")
    return redirect(url_for('index'))


def upvote_answer():
    flash("Redirected from upvote_answer()")
    return redirect(url_for('index'))
