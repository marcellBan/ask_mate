import hashlib

from flask import flash, render_template, request, redirect, session, url_for

import comment_data_manager
import answer_data_manager
import question_data_manager


def login_required(func_that_needs_login):
    def logged_in_check(*args, **kwargs):
        user = session.get('user_name')
        if user is None:
            session['prev'] = request.url
            return redirect(url_for('login'))
        return func_that_needs_login(*args, **kwargs)
    return logged_in_check


def author_user_required(func, entry_type):
    def author_check(*args, **kwargs):
        if entry_type == 'question':
            entry = question_data_manager.get_question(args[0])
        elif entry_type == 'answer':
            entry = answer_data_manager.get_answer(args[0])
        elif entry_type == 'comment':
            entry = comment_data_manager.get_comment(args[0])
        if entry.get('user_name') != session.get('user_name'):
            flash('You don\' have permission for this operation!')
            return redirect(session.get('prev'))
        else:
            return func(*args, **kwargs)
    return author_check


def hash_password(password):
    '''Return a string of a hashed password'''
    hashing = hashlib.sha1()
    hashing.update(bytes(password, 'utf-8'))
    return hashing.hexdigest()


def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':

        # TODO check existing users in database, usernames must be unique
        username_taken = False

        user_name = request.form.get('user_name')
        password = request.form.get('password')
        password_check = request.form.get('password_check')
        # user_name error checking
        if user_name is None:
            flash('Please enter a username!')
            return render_template('register.html')
        elif len(user_name) < 4:
            flash('Your username isn\'t long enough!')
            return render_template('register.thml')
        # TODO check existing users in database, usernames must be unique
        elif username_taken:
            flash('That username is already taken!')
            return render_template('register.html')
        # password error_checking
        elif password is None or password_check is None:
            flash('Please enter a password!')
            return render_template('register.html', form_user_name=user_name)
        elif len(password) < 6:
            flash('Your password isn\'t long enough!')
            return render_template('register.html', form_user_name=user_name)
        elif password != password_check:
            flash('The two passwords don\'t match!')
            return render_template('register.html', form_user_name=user_name)
        password = hash_password(password)
        flash('Successfully registered!')
        # TODO update users table.
        # TODO user should be redirected based on session data.
        session['user_name'] = user_name
        return redirect(url_for('index'))


def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':

        # TODO check database for credential information
        correct_credentials = True

        user_name = request.form.get('user_name')
        password = request.form.get('password')
        if user_name is None:
            flash('Please enter your username!')
            return render_template('login.html')
        elif password is None:
            flash('Please enter your password!')
            return render_template('login.html', form_user_name=user_name)
        password = hash_password(password)
        # TODO query matching user_name and password from database
        if not correct_credentials:
            flash('The credential information you entered was incorrect!')
            return render_template('login.html', form_user_name=user_name)
        # TODO update session data.
        # TODO user should be redirected based on session data.
        return redirect(url_for('index'))


def logout():
    if session.get('user_name'):
        session.pop('user_name')
    return redirect(url_for('index'))
