'''work with ingredients'''
import json
from flask import render_template, session, request
from flask.views import MethodView
from __init__ import users, dbrecipes
from additional_functions import find_with_majority_ingredients

recipes = []
liked_recipes = []

class TinderView(MethodView):
    '''Tinder'''
    def get(self):
        '''open tinder'''
        return render_template('tinder.html', recipes=recipes)

class IngredientsView(MethodView):
    '''Ingredients'''
    def get(self):
        '''open ingredients'''
        return render_template('ingredients.html', liked_recipes=liked_recipes)

class StoreDataView(MethodView):
    '''StoreData'''
    def post(self):
        '''Storing Data'''
        global recipes
        data = request.data
        data = json.loads(data)
        session['selected_ingredients'] = data
        recipes = find_with_majority_ingredients(data, 0.4) if data else []
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
            for meal in liked_recipes:
                liked_meal = {'Ingredients': meal[2],
                                       'Instructions': meal[3],
                                       'Image_Name': f"{meal[0]}.jpg",
                                       'Rating': 0}
                users.update_one({'email': user_email}, {'$set': {f'liked.{meal[1]}': liked_meal}})
        return "", 200

class RecipeView(MethodView):
    '''RecipeView'''
    def get(self, recipe_id):
        '''RecipePage'''
        user_email = session.get('email')
        if not user_email:
            return render_template('login.html')
        recipe = dbrecipes.find_one({"Image_Name": recipe_id[:-4]})
        user = users.find_one({"email": user_email})
        liked = user['liked']
        for like, listik in liked.items():
            if recipe_id == listik['Image_Name']:
                recipe = (like, user['liked'][like])
        if not recipe:
            return 'Recipe not found', 40
        return render_template('recipe.html', recipe=recipe)
