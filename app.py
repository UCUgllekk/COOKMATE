'''app.py'''
import secrets
import json
import re
from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask.views import MethodView
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

secret_key = secrets.token_hex(16)

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://pavlosiukpn:U221Bd9n@cookma"+\
    "tecluster.uqlmdxd.mongodb.net/python_project"
app.secret_key = secret_key

mongo = PyMongo(app)
records = mongo.db.users
recipes = []
liked_recipes = []

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
        # if 'email' in session:
        #     return redirect(url_for('Si'))
        return render_template('sign_up.html', message='')

    def post(self):
        '''SignUp'''
        email = request.form.get('email')
        if validate_email(email):
            password = request.form.get('password')
            if validate_password(password) == True:
                if not email or not password:
                    return render_template('sign_up.html', message='Please fill in all the fields')
                if records.find_one({'email': email}):
                    return render_template('sign_up.html', message='User already exists!')
                hashed = generate_password_hash(password, method='scrypt')
                user_input = {'email': email, 'password': hashed, 'liked': {}, \
                    'rated': {}}
                records.insert_one(user_input)
                session['email'] = email
                return redirect(url_for('liked'))
            return render_template('sign_up.html', message=validate_password(password))
        return render_template('sign_up.html', message='Wrong email form')

class IngredientsView(MethodView):
    '''Ingredients'''
    def get(self):
        '''open ingredients'''
        print(liked_recipes)
        return render_template('ingredients.html', liked_recipes=liked_recipes)

class TinderView(MethodView):
    '''Tinder'''
    def get(self):
        '''open tinder'''
        return render_template('tinder.html', recipes=recipes)

class LikedView(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        if 'email' in session:
            user_email = session.get('email')
            user = mongo.db.users.find_one({"email": user_email})
            liked = user['liked']
            users = mongo.db.users
            for liked_recipe, data in liked.items():
                # print(data)
                if liked_recipe in user['rated']:
                    new_liked = {'Ingredients': data['Ingredients'],
                                 'Instructions': data['Instructions'],
                                 'Image_Name': data['Image_Name'],
                                 'Rating': user['rated'][liked_recipe]['Rating']}
                    users.update_one({'email': user_email}, {'$set': {f'liked.{liked_recipe}': new_liked}})
            print(user['liked'])
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

class RatedView(MethodView):
    '''View Recipes'''
    def get(self):
        '''Recipes'''
        user_email = session.get('email')
        if not user_email:
            return render_template('login.html')
        user = mongo.db.users.find_one({"email": user_email})
        rated_recipes = user['rated']
        print(rated_recipes)
        return render_template('rated.html', recipes=rated_recipes)

class StoreDataView(MethodView):
    '''StoreData'''
    def post(self):
        '''Storing Data'''
        global recipes
        data = request.data
        data = json.loads(data)
        print(f"{data=}")
        session['selected_ingredients'] = data
        recipes = find_with_majority_ingredients(data, 0.5) if data else []
        print()
        print("stored")
        return "", 200

class StoreLikedRecipesView(MethodView):
    '''StoreLikedRecipes'''
    def post(self):
        '''Storing liked recipes'''
        global liked_recipes
        data = request.data
        data = json.loads(data)
        liked_recipes = data
        user_email = session.get('email')
        if user_email:
            users = mongo.db.users
            for meal in liked_recipes:
                liked_meal = {'Ingredients': meal[2],
                                       'Instructions': meal[3],
                                       'Image_Name': f"{meal[0]}.jpg",
                                       'Rating': 0}
                users.update_one({'email': user_email}, {'$set': {f'liked.{meal[1]}': liked_meal}})
            # user = users.find_one({"email": user_email})
            # print(user)
        return "", 200

class RecipeView(MethodView):
    '''RecipeView'''
    def get(self, recipe_id):
        '''RecipePage'''
        user_email = session.get('email')  # Get the email from the session
        if not user_email:
            return render_template('login.html')
        user = mongo.db.users.find_one({"email": user_email})
        liked = user['liked']
        for like, listik in liked.items():
            if recipe_id == listik['Image_Name']:
                recipe = (like, user['liked'][like])
        print(type(recipe), recipe)
        if not recipe:
            return 'Recipe not found', 40
        return render_template('recipe.html', recipe=recipe)

class RateView(MethodView):
    '''RateView'''
    def post(self):
        '''Set Rate'''
        user_email = session.get('email')
        if not user_email:
            return render_template('login.html')
        data = request.data
        data = json.loads(data)
        recipe = mongo.db.recipes.find_one({'Title': data['recipe']})
        users = mongo.db.users
        rating = int(data['rating'])
        rated_recipe = {'Ingredients': recipe['Ingredients'],
                        'Instructions': recipe['Instructions'],
                        'Image_Name': recipe['Image_Name'] + '.jpg',
                        'Rating': rating}
        users.update_one({'email': user_email}, {'$set': \
            {f"rated.{recipe['Title']}": rated_recipe}})
        # user = users.find_one({"email": user_email})
        # print(user)
        return 'Success', 200

def validate_password(password: str):
    '''password'''
    if len(password) < 8:
        return "Password should contain eight symbols"
    if not bool(re.fullmatch(r"^(?=.*?[A-Z]).*$", password)):
        return "Password should contain at least one capital letter"
    if not bool(re.fullmatch(r"^(?=.*?[a-z]).*$", password)):
        return "Password should contain at least one lowercase letter"
    if not bool(re.fullmatch(r"^(?=.*?[0-9]).*$", password)):
        return "Password should contain at least one digit"
    if not bool(re.fullmatch(r"^(?=.*?[#?!@$%^&*_-]).*$", password)):
        return "Password should contain at least one of these symbols: #?!@$%^&*_-"
    return True
    # return bool(re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])"+\
    #     r"(?=.*?[#?!@$%^&*_-]).{8,}$", password))

def validate_email(email:str):
    '''email'''
    return bool(re.fullmatch(r"^(?!\.)[a-z!#$%&'*+\-/=?^_`{|}~]+(?:\.[a-z!#$%&'*+\-/=?^_`"+\
        r"{|}~]{1,64})*@[a-z]{1,255}(\.(gmail|ucu|com|org|edu|gov|net|ua))+", email))

def find_with_majority_ingredients(ingredient_list, amount: float):
    '''Find recipes by ingredients'''
    all_docs = mongo.db.recipes.find({}, {"Cleaned_Ingredients": 1, "Image_Name": 1, \
        "Title": 1, "Ingredients": 1, 'Instructions': 1})
    matching_docs = []
    print("docs: ", all_docs)
    for doc in all_docs:
        doc_ingredients = doc['Cleaned_Ingredients'][2:-2].split("', '")
        common_ingredients = set(doc_ingredients) & set(ingredient_list)
        if len(common_ingredients) / len(doc_ingredients) > amount:
            print(doc_ingredients, common_ingredients)
            matching_docs.append(doc['Image_Name'])
            matching_docs.append(doc['Title'])
            matching_docs.append(doc['Ingredients'])
            matching_docs.append(doc['Instructions'])
    return matching_docs

app.add_url_rule('/', view_func=MainView.as_view('main_page'))
app.add_url_rule('/ingredients', view_func=IngredientsView.as_view('ingredients'))
app.add_url_rule('/login', view_func=LoginView.as_view('log_in'))
app.add_url_rule('/sign_up', view_func=SignUpView.as_view('sign_up'))
app.add_url_rule('/search', view_func=SearchView.as_view('search_view'))
app.add_url_rule('/tinder', view_func=TinderView.as_view('tinder'))
app.add_url_rule('/liked', view_func=LikedView.as_view('liked'))
app.add_url_rule('/store_data', view_func=StoreDataView.as_view('store_data'))
app.add_url_rule('/store_liked_recipes', view_func=StoreLikedRecipesView.as_view('store_liked_recipes'))
app.add_url_rule('/rated', view_func=RatedView.as_view('recipes'))
app.add_url_rule('/rate', view_func=RateView.as_view('rate'))
app.add_url_rule('/recipe/<recipe_id>/', view_func=RecipeView.as_view('recipe'))

if __name__ == '__main__':
    app.run(debug=True)
