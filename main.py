'''
AskMate Q&A website
by SzószKód
'''
from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index, all questions with default sorting.'


@app.route('/sort')
def sorted_index():
    return 'Index, sorted by time={} & title={}.'.format(request.args.get('time', request.args.get('title')))


@app.route('/question/new', methods=['GET', 'POST'])
def new_question():
    return 'New question.'


@app.route('/question/<int:q_id>')
def display_question(q_id=0):
    return 'Display question with id {}.'.format(q_id)


@app.route('/question/<int:q_id>/new-answer', methods=['GET', 'POST'])
def new_answer(q_id=0):
    return 'New answer to question with id {}.'.format(q_id)


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


if __name__ == "__main__":
    app.run(debug=True)
