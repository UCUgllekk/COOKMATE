'''login, logout, signup'''
from flask import render_template, request, redirect, session, url_for
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from additional_functions import validate_email, validate_password
from __init__ import users

class LoginView(MethodView):
    '''Login'''
    def get(self):
        '''LoginPage'''
        if 'email' in session:
            return redirect(url_for('liked'))
        return render_template('login.html', message='')

    def post(self):
        '''Login'''
        email = request.form.get('email')
        password = request.form.get('password')
        user_found = users.find_one({'email': email})
        if user_found:
            user_val = user_found['email']
            passwordcheck = user_found['password']
            if check_password_hash(passwordcheck, password):
                session['email'] = user_val
                return redirect(url_for('liked'))
            return render_template('login.html', message='Wrong Password!')
        return render_template('login.html', message='User does not exist!')

class LogoutView(MethodView):
    '''Logout'''
    def get(self):
        '''LogoutPage'''
        if 'email' in session:
            session.pop('email', None)
        return redirect(url_for('log_in'))

class SignUpView(MethodView):
    '''SignUp'''
    def get(self):
        '''SignUpPage'''
        return render_template('sign_up.html', message='')

    def post(self):
        '''SignUp'''
        email = request.form.get('email')
        if validate_email(email):
            password = request.form.get('password')
            if validate_password(password) == True:
                if not email or not password:
                    return render_template('sign_up.html', message='Please fill in all the fields')
                if users.find_one({'email': email}):
                    return render_template('sign_up.html', message='User already exists!')
                hashed = generate_password_hash(password, method='scrypt')
                user_input = {'email': email, 'password': hashed, 'liked': {}, \
                    'rated': {}}
                users.insert_one(user_input)
                session['email'] = email
                return redirect(url_for('liked'))
            return render_template('sign_up.html', message=validate_password(password))
        return render_template('sign_up.html', message='Wrong email form')
