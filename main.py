'''AskMate Q&A website
by SzószKód
'''
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index, all questions with default sorting.'


@app.route('/sort-by=<sort_type>')
def sorted_index(sort_type):
    return 'Index, sorted by %s.' % sort_type


@app.route('/question/new')
def new_question():
    return 'New question.'


@app.route('/question/<int:q_id>')
def display_question(q_id=0):
    return 'Display question with id %s.' % q_id


@app.route('/question/<int:q_id>/new-answer')
def new_answer(q_id=0):
    return 'New answer to question with id %s.' % q_id


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == "__main__":
    app.run('0.0.0.0')
