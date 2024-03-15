'''app.py'''
import secrets
import re
from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask.views import MethodView
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

secret_key = secrets.token_hex(16)

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://pavlosiukpn:U221Bd9n@cookmatecluster.uqlmdxd.mongodb.net/python_project"
app.secret_key = secret_key

mongo = PyMongo(app)
records = mongo.db.users

class MainView(MethodView):
    '''MainPage'''
    def get(self):
        '''open_main_page'''
        return render_template('main_page.html')

class SearchView(MethodView):
    '''SearchView'''
    def get(self):
        '''Search'''
        query = request.args.get('query')
        results = mongo.db.ingredients.find({"name": {"$regex": query.strip()}})
        suggestions = sorted([result['name'] for result in results], key=len)
        return jsonify(suggestions)

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
        user_found = records.find_one({'email': email})
        if user_found:
            user_val = user_found['email']
            passwordcheck = user_found['password']
            if check_password_hash(passwordcheck, password):
                session['email'] = user_val
                return redirect(url_for('liked'))
            return render_template('login.html', message='Wrong Password!')
        return render_template('login.html', message='User does not exist!')

class SignUpView(MethodView):
    '''SignUp'''
    def get(self):
        '''SignUpPage'''
        if 'email' in session:
            return redirect(url_for('profile'))
        return render_template('sign_up.html', message='')

    def post(self):
        '''SignUp'''
        email = request.form.get('email')
        if validate_email(email):
            password = request.form.get('password')
            if not email or not password:
                return render_template('sign_up.html', message='Please fill in all the fields')
            if records.find_one({'email': email}):
                return render_template('sign_up.html', message='User already exists!')
            hashed = generate_password_hash(password, method='scrypt')
            user_input = {'email': email, 'password': hashed, 'liked': [], \
                'rated': {'5':{}, "4":{}, '3':{}, '2':{}, '1':{}, '0':{}}}
            records.insert_one(user_input)
            session['email'] = email
            return redirect(url_for('liked'))
        return render_template('sign_up.html', message='Wrong email form')

class IngredientsView(MethodView):
    '''Ingredients'''
    def get(self):
        '''open ingredients'''
        return render_template('ingredients.html')

class ProfileView(MethodView):
    '''Profile'''
    def get(self):
        '''open profile'''
        return render_template('profile.html')

class TinderView(MethodView):
    '''Tinder'''
    def get(self):
        '''open tinder'''
        return render_template('tinder.html')

class LikedView(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        return render_template('liked.html')

class RatedView(MethodView):
    '''Rated'''
    def get(self):
        '''open rated'''
        return render_template('rated.html')

def validate_email(email:str):
    '''email'''
    return bool(re.fullmatch(r"^(?!\.)[a-z!#$%&'*+\-/=?^_`{|}~]+(?:\.[a-z!#$%&'*+\-/=?^_`"+\
        r"{|}~]{1,64})*@[a-z]{1,255}(\.(gmail|ucu|com|org|edu|gov|net|ua))+", email))

app.add_url_rule('/', view_func=MainView.as_view('main_page'))
app.add_url_rule('/ingredients', view_func=IngredientsView.as_view('ingredients'))
app.add_url_rule('/login', view_func=LoginView.as_view('log_in'))
app.add_url_rule('/sign_up', view_func=SignUpView.as_view('sign_up'))
app.add_url_rule('/search', view_func=SearchView.as_view('search_view'))
app.add_url_rule('/tinder', view_func=TinderView.as_view('tinder'))
app.add_url_rule('/rated', view_func=RatedView.as_view('rated'))
app.add_url_rule('/liked', view_func=LikedView.as_view('liked'))

if __name__ == '__main__':
    app.run(debug=True)
