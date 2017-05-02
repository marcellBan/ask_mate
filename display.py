'''
Display the questions from questions.csv file
For AskMate by SzószKód
'''

from data_manager import load_data
from flask import render_template


def display_questions():
    data = load_data()
    return render_template('.html')