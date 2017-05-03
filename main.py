'''
AskMate Q&A website
by SzószKód
'''
# flash import can be deleted later on.
from flask import Flask, request, render_template, flash

import display
import entry_manager
app = Flask(__name__)
app.secret_key = 'I have no idea what I\'m doing'


@app.route('/')
def index():
    return display.display_questions()


@app.route('/sort')
def sorted_index():
    return display.display_sorted_questions()


@app.route('/question/new', methods=['GET', 'POST'])
def new_question():
    return entry_manager.add_question()


@app.route('/question/<int:q_id>')
def display_question(q_id=0):
    return display.display_one_question(q_id)


@app.route('/question/<int:q_id>/new-answer', methods=['GET', 'POST'])
def new_answer(q_id=0):
    return entry_manager.add_answer(q_id)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == "__main__":
    app.run(debug=True)
