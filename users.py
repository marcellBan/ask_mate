import hashlib

from flask import flash, render_template, request, redirect, session


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
        elif len(user_name) > 4:
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
        elif len(password) > 6:
            flash('Your password isn\'t long enough!')
            return render_template('register.html', form_user_name=user_name)
        elif password != password_check:
            flash('The two passwords don\'t match!')
            return render_template('register.html', form_user_name=user_name)
        hashing = hashlib.sha1()
        hashing.update(bytes(password, 'utf-8'))
        password = hashing.hexdigest()
        print(password)
        return render_template('register.html')


def login_required(func_that_needs_login):
    def logged_in_check(*args, **kwargs):
        user = session.get('user_name')
        if user is None:
            return redirect(session.get('prev'))
        return func_that_needs_login(*args, **kwargs)
    return logged_in_check
