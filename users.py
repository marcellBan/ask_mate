import hashlib
import time

from flask import flash, render_template, request, redirect, session, url_for

import users_data_manager


def hash_password(password):
    '''Return a string of a hashed password'''
    hashing = hashlib.sha1()
    hashing.update(bytes(password, 'utf-8'))
    return hashing.hexdigest()


def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
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
        elif users_data_manager.username_exists(user_name):
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
        user_data = {
            'user_name': user_name,
            'password': password,
            'registration_date': int(time.time())
        }
        flash('Successfully registered!')
        users_data_manager.new_user(user_data)
        session['user_name'] = user_name
        return redirect(session.get('prev'))


def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        if user_name is None:
            flash('Please enter your username!')
            return render_template('login.html')
        elif password is None:
            flash('Please enter your password!')
            return render_template('login.html', form_user_name=user_name)
        password = hash_password(password)
        user_data = {
            'user_name': user_name,
            'password': password
        }
        if not users_data_manager.correct_credentials(user_data):
            flash('The credential information you entered was incorrect!')
            return render_template('login.html', form_user_name=user_name)
        session['user_name'] = user_name
        return redirect(session.get('prev'))


def logout():
    if session.get('user_name'):
        session.pop('user_name', None)
    return redirect(url_for('index'))
