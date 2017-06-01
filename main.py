'''
AskMate Q&A website
by SzószKód
'''
from flask import Flask
from jinja2 import evalcontextfilter, Markup
import datetime

import display
import answer_entry_manager
import comment_entry_manager
import question_entry_manager
import vote
import users
app = Flask(__name__)
app.secret_key = 'I have no idea what I\'m doing'


@app.route('/')
def index():
    return display.display_five_latest_questions()


@app.route('/list')
def list_index():
    return display.display_questions()


@app.route('/sort')
def sorted_index():
    return display.display_sorted_questions()


@app.route('/sort/clear')
def clear_sort():
    return display.clear_sorting()


@app.route('/question/new', methods=['GET', 'POST'])
@users.login_required
def new_question():
    return question_entry_manager.add_question()


@app.route('/question/<int:question_id>')
def display_question(question_id):
    return display.display_one_question(question_id)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
@users.login_required
@users.author_user_required('question')
def question_edit(question_id):
    return question_entry_manager.edit_question(question_id)


@app.route('/question/<int:question_id>/delete')
@users.login_required
@users.author_user_required('question')
def question_delete(question_id):
    return question_entry_manager.delete_question(question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
@users.login_required
def new_answer(question_id):
    return answer_entry_manager.add_answer(question_id)


@app.route('/question/<int:question_id>/vote-down')
@users.login_required
def downvote_question(question_id):
    return vote.downvote_question(question_id)


@app.route('/question/<int:question_id>/vote-up')
@users.login_required
def upvote_question(question_id):
    return vote.upvote_question(question_id)


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
@users.login_required
def new_comment_for_question(question_id):
    return comment_entry_manager.new_comment_for_question(question_id)


@app.route('/answer/<int:answer_id>/vote-down')
@users.login_required
def downvote_anwer(answer_id):
    return vote.downvote_answer(answer_id)


@app.route('/answer/<int:answer_id>/vote-up')
@users.login_required
def upvote_answer(answer_id):
    return vote.upvote_answer(answer_id)


@app.route('/answer/<int:answer_id>/delete')
@users.login_required
@users.author_user_required('answer')
def answer_delete(answer_id):
    return answer_entry_manager.delete_answer(answer_id)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
@users.login_required
@users.author_user_required('answer')
def answer_edit(answer_id):
    return answer_entry_manager.edit_answer(answer_id)


@app.route('/answer/<int:answer_id>/accepted')
def accept_answer():
    return answer_entry_manager.accepted_answer(answer_id)


@app.route('/comments/<int:comment_id>/delete')
@users.login_required
@users.author_user_required('comment')
def comment_delete(comment_id):
    return comment_entry_manager.delete_comment(comment_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
@users.login_required
def new_comment_for_answer(answer_id):
    return comment_entry_manager.new_comment_for_answer(answer_id)


@app.route('/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
@users.login_required
@users.author_user_required('comment')
def edit_comment(comment_id):
    return comment_entry_manager.edit_comment(comment_id)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    return users.register()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return users.login()


@app.route('/logout')
def logout():
    return users.logout()


@app.errorhandler(404)
def page_not_found(error):
    return 'Oops, page not found!', 404


@app.template_filter('time')
def _jinja2_time_filter(value):
    time = datetime.datetime.fromtimestamp(value)
    result = '{:02}-{:02}-{} {}:{:02}'.format(time.day, time.month, time.year, time.hour, time.minute)
    return result


if __name__ == "__main__":
    app.run()
