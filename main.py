'''
AskMate Q&A website
by SzószKód
'''
from flask import Flask, session, request, redirect, url_for, flash
from jinja2 import evalcontextfilter, Markup
import datetime

import display
import answer_entry_manager
import comment_entry_manager
import question_entry_manager
import comment_data_manager
import answer_data_manager
import question_data_manager
import vote
import users
app = Flask(__name__)
app.secret_key = 'I have no idea what I\'m doing'


@app.before_request
def login_required():
    url_parts = request.url.split('/')
    login_valid = 'user_name' in session
    is_public = getattr(app.view_functions[request.endpoint], 'is_public', False)
    # don't show login/register when logged in
    if (login_valid and url_parts[-1] in ('registration', 'login')):
        flash('You can\'t do that while logged in!')
        return redirect(session.get('prev'))
    # not logged in redirect to login
    if (not login_valid and not is_public and 'static' not in url_parts):
        session['prev'] = request.url
        flash('You need to log in to do that.')
        return redirect(url_for('login'))
    # check if user is the author
    if url_parts[-1] in ('edit', 'delete'):
        entry_id = int(url_parts[-2])
        entry_type = url_parts[-3]
        if entry_type == 'question':
            entry = question_data_manager.get_question(entry_id)
        elif entry_type == 'answer':
            entry = answer_data_manager.get_answer(entry_id)
        elif entry_type == 'comment':
            entry = comment_data_manager.get_comment(entry_id)
        if entry.get('user_name') != session.get('user_name'):
            flash('You don\' have permission for this operation!')
            return redirect(session.get('prev'))


def public(func):
    func.is_public = True
    return func


@public
@app.route('/')
def index():
    return display.display_five_latest_questions()


@public
@app.route('/list')
def list_index():
    return display.display_questions()


@public
@app.route('/sort')
def sorted_index():
    return display.display_sorted_questions()


@public
@app.route('/sort/clear')
def clear_sort():
    return display.clear_sorting()


@app.route('/question/new', methods=['GET', 'POST'])
def new_question():
    return question_entry_manager.add_question()


@public
@app.route('/question/<int:question_id>')
def display_question(question_id):
    return display.display_one_question(question_id)


@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def question_edit(question_id):
    return question_entry_manager.edit_question(question_id)


@app.route('/question/<int:question_id>/delete')
def question_delete(question_id):
    return question_entry_manager.delete_question(question_id)


@app.route('/question/<int:question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    return answer_entry_manager.add_answer(question_id)


@app.route('/question/<int:question_id>/vote-down')
def downvote_question(question_id):
    return vote.downvote_question(question_id)


@app.route('/question/<int:question_id>/vote-up')
def upvote_question(question_id):
    return vote.upvote_question(question_id)


@app.route('/question/<int:question_id>/new-comment', methods=['GET', 'POST'])
def new_comment_for_question(question_id):
    return comment_entry_manager.new_comment_for_question(question_id)


@app.route('/answer/<int:answer_id>/vote-down')
def downvote_anwer(answer_id):
    return vote.downvote_answer(answer_id)


@app.route('/answer/<int:answer_id>/vote-up')
def upvote_answer(answer_id):
    return vote.upvote_answer(answer_id)


@app.route('/answer/<int:answer_id>/delete')
def answer_delete(answer_id):
    return answer_entry_manager.delete_answer(answer_id)


@app.route('/answer/<int:answer_id>/edit', methods=['GET', 'POST'])
def answer_edit(answer_id):
    return answer_entry_manager.edit_answer(answer_id)


@app.route('/comments/<int:comment_id>/delete')
def comment_delete(comment_id):
    return comment_entry_manager.delete_comment(comment_id)


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET', 'POST'])
def new_comment_for_answer(answer_id):
    return comment_entry_manager.new_comment_for_answer(answer_id)


@app.route('/comments/<int:comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    return comment_entry_manager.edit_comment(comment_id)


@public
@app.route('/registration', methods=['GET', 'POST'])
def register():
    return users.register()


@public
@app.route('/login', methods=['GET', 'POST'])
def login():
    return users.login()


@app.route('/logout')
def logout():
    return users.logout()


@app.route('/users')
def list_users():
    return display.list_users()


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
