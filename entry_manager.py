'''
entry manager module for AskMate
by SzószKód
'''

from flask import render_template, redirect, request


def add_question():
    return render_template("new_question.html")
