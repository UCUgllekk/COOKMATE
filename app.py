'''app.py'''
from flask import Flask, render_template, request, redirect, jsonify, session
from flask.views import MethodView
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://pavlosiukpn:U221Bd9n@cookmatecluster.uqlmdxd.mongodb.net/python_project"
app.secret_key = 'helloworld+:>"LKHL'

mongo = PyMongo(app)

class MainPage(MethodView):
    '''MainPage'''
    def get(self):
        '''open_main_page'''
        return render_template('main_page.html')

class LoginPage(MethodView):
    '''LoginPage'''
    def get(self):
        '''open login'''
        return render_template('login.html')

class SignUpPage(MethodView):
    '''SingUpPage'''
    def get(self):
        '''open sign up'''
        return render_template('sign_up.html')

class IngredientsPage(MethodView):
    '''Ingredients'''
    def get(self):
        '''open ingredients'''
        return render_template('ingredients.html')

# class ProfilePage(MethodView):
#     '''Profile'''
#     def get(self):
#         '''open profile'''
#         return render_template('profile.html')

class TinderPage(MethodView):
    '''Tinder'''
    def get(self):
        '''open tinder'''
        return render_template('tinder.html')

class LikedPage(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        return render_template('liked.html')

class RatedPage(MethodView):
    '''Rated'''
    def get(self):
        '''open rated'''
        return render_template('rated.html')

# class StoreDataView(MethodView):
#     def get(self):
#         data = request.data
#         data = json.loads(data)
#         # Now data is a Python list
#         # Store it in the session
#         print(f"{data=}")
#         session['selected_ingredients'] = data
#         found_recipes = find_with_majority_ingredients(data, 0.5)
#         return '', 200  # Return found_recipes in the response

class StoreDataView(MethodView):
    def post(self):
        data = request.data
        data = json.loads(data)
        print(session)
        session['selected_ingredients'] = data
        print(session)
        found_recipes = find_with_majority_ingredients(data, 0.5)
        return jsonify(found_recipes), 200

class StoreDataView(MethodView):
    def get(self):
        selected_ingredients = session.get('selected_ingredients', [])

def find_with_majority_ingredients(ingredient_list, amount: float):
    all_docs = mongo.db.recipes.find({}, {"Cleaned_Ingredients": 1, "Image_Name": 1, "Title": 1})  # only return the 'cleaned_ingredients' field
    matching_docs = []
    print("docs: ", all_docs)
    for doc in all_docs:
        doc_ingredients = doc['Cleaned_Ingredients'][2:-2].split("', '")  # assuming ingredients are comma-separated
        common_ingredients = set(doc_ingredients) & set(ingredient_list)
        if len(common_ingredients) / len(doc_ingredients) > amount:
            matching_docs.append(doc['Image_Name'])
    return matching_docs

app.add_url_rule('/', view_func=MainPage.as_view('main_page'))
app.add_url_rule('/ingredients', view_func=IngredientsPage.as_view('ingredients'))
# app.add_url_rule('/profile', view_func=ProfilePage.as_view('profile'))
app.add_url_rule('/login', view_func=LoginPage.as_view('login'))
app.add_url_rule('/sign_up', view_func=SignUpPage.as_view('sign_up'))
app.add_url_rule('/search', view_func=SearchView.as_view('search_view'))
app.add_url_rule('/tinder', view_func=TinderPage.as_view('tinder'))
app.add_url_rule('/store_data', view_func=StoreDataView.as_view('store_data'))
app.add_url_rule('/liked', view_func=StoreDataView.as_view('liked'))
app.add_url_rule('/rated', view_func=StoreDataView.as_view('rated'))

if __name__ == '__main__':
    app.run(debug=True)
