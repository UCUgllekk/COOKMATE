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

app.config["MONGO_URI"] = "mongodb+srv://pavlosiukpn:U221Bd9n@cookmatecluster.uqlmdxd.mongodb.net/python_project"
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
        if 'email' in session:
            return redirect(url_for('profile'))
        return render_template('sign_up.html', message='')

    def post(self):
        '''SignUp'''
        email = request.form.get('email')
        if validate_email(email):
            password = request.form.get('password')
            if validate_password(password):
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
            return render_template('sign_up.html', message='Wrong password form')
        return render_template('sign_up.html', message='Wrong email form')

class IngredientsView(MethodView):
    '''Ingredients'''
    def get(self):
        '''open ingredients'''
        print(liked_recipes)
        return render_template('ingredients.html', liked_recipes=liked_recipes)

class ProfileView(MethodView):
    '''Profile'''
    def get(self):
        '''open profile'''
        return render_template('profile.html')

class TinderView(MethodView):
    '''Tinder'''
    def get(self):
        '''open tinder'''
        # print(session['recipes'])
        # recipes = session['recipes'] if "recipes" in session else []
        return render_template('tinder.html', recipes=recipes)

class LikedView(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        user_email = session.get('email')
        user = mongo.db.users.find_one({"email": user_email})
        liked_recipes = user['liked']
        print(liked_recipes)
        return render_template('liked.html', recipes = liked_recipes)

class RatedView(MethodView):
    '''View Recipes'''
    def get(self):
        '''Recipes'''
        print('im in recipeview get')
        user_email = session.get('email')
        if not user_email:
            return render_template('login.html')
        user = mongo.db.users.find_one({"email": user_email})
        rated_recipes = user['liked']
        recipes = [mongo.db.recipes.find_one({"id": recipe[0]}) for recipe in rated_recipes]
        return render_template('rated.html', recipes=recipes)

# class RateView(MethodView):
#     '''Rating'''
#     def post(self):
#         '''Ra'''
#         print('im in rateview post')
#         user_email = session.get('email')
#         if not user_email:
#             return render_template('login.html')
#         recipe_id = request.form.get('recipe_id')
#         rating = request.form.get('rating')
#         user = mongo.db.users.find_one({"email": user_email})
#         user['rated'] = [meal for meal in user['rated'] if meal['id'] != recipe_id]
#         user['rated'].append({'id': recipe_id, 'rating': rating})
#         mongo.db.users.save(user)
#         return 'Success', 200

def validate_password(password: str):
    '''password'''
    return bool(re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password))

def validate_email(email:str):
    '''email'''
    return bool(re.fullmatch(r"^(?!\.)[a-z!#$%&'*+\-/=?^_`{|}~]+(?:\.[a-z!#$%&'*+\-/=?^_`"+\
        r"{|}~]{1,64})*@[a-z]{1,255}(\.(gmail|ucu|com|org|edu|gov|net|ua))+", email))

class StoreDataView(MethodView):
    '''StoreData'''
    def post(self):
        '''Storing Data'''
        global recipes
        data = request.data
        data = json.loads(data)
        print(f"{data=}")
        session['selected_ingredients'] = data
        recipes = find_with_majority_ingredients(data, 0.5)
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
                                       'Image_Name': f"{meal[0]}.jpg"}
                # user['liked'].append(liked_meal)
                users.update_one({'email': user_email}, {'$push': {f'liked.{meal[1]}': liked_meal}})
            users.find_one({"email": user_email})
        return "", 200

class RecipeView(MethodView):
        '''RecipeView'''
        def get(self, recipe_id):
            '''RecipePage'''
            recipe = mongo.db.recipes.find_one({"Image_Name": recipe_id[:-4]})
            print(recipe)
            if not recipe:
                return 'Recipe not found', 404
            return render_template('recipe.html', recipe=recipe)

class RateView(MethodView):
    '''RateView'''
    def post(self):
        '''Set Rate'''
        user_email = session.get('email')  # Get the email from the session
        if not user_email:
            return render_template('login.html')

        rating = request.form.get('rating')
        recipe = request.form.get('recipe')
        user = mongo.db.users.find_one({"email": user_email})
        user['rated'] = (recipe, rating)
        mongo.db.users.save(user)
        return 'Success', 200

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
