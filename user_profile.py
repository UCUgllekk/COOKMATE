'''user profile'''
import json
from flask import render_template, session, request
from flask.views import MethodView
from __init__ import users, dbrecipes

class LikedView(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            liked = user['liked']
            for liked_recipe, data in liked.items():
                if liked_recipe in user['rated']:
                    new_liked = {'Ingredients': data['Ingredients'],
                                    'Instructions': data['Instructions'],
                                    'Image_Name': data['Image_Name'],
                                    'Rating': user['rated'][liked_recipe]['Rating']}
                    users.update_one({'email': user_email}, {'$set': {f'liked.{liked_recipe}':\
                        new_liked}})
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

    def post(self):
        '''Like'''
        user_email = session.get('email')
        user = users.find_one({"email": user_email})
        liked = user['liked']
        sort_type = request.form.get('knopka')
        if sort_type == 'name':
            liked = dict(sorted(liked.items()))
        elif sort_type == 'amount':
            liked = dict(sorted(liked.items(), key=lambda x: len(x[1]['Ingredients'])))
        return render_template('liked.html', recipes = liked)


class RatedView(MethodView):
    '''View Recipes'''
    def get(self):
        '''Recipes'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            rated_recipes = user['rated']
            return render_template('rated.html', recipes=rated_recipes)
        return render_template('login.html')

    def post(self):
        '''Like'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            rated = user['liked']
            sort_type = request.form.get('knopka')
            if sort_type == '1 star':
                rated = {name:parameters for name,parameters in rated.items() \
                    if parameters['Rating'] == 1}
            elif sort_type == '2 star':
                rated = {name:parameters for name,parameters in rated.items() \
                    if parameters['Rating'] == 2}
            elif sort_type == '3 star':
                rated = {name:parameters for name,parameters in rated.items() \
                    if parameters['Rating'] == 3}
            elif sort_type == '4 star':
                rated = {name:parameters for name,parameters in rated.items() \
                    if parameters['Rating'] == 4}
            elif sort_type == '5 star':
                rated = {name:parameters for name,parameters in rated.items() \
                    if parameters['Rating'] == 5}
            return render_template('rated.html', recipes = rated)
        return render_template('login.html')


class RateView(MethodView):
    '''RateView'''
    def post(self):
        '''Set Rate'''
        user_email = session.get('email')
        data = request.data
        data = json.loads(data)
        recipe = dbrecipes.find_one({'Title': data['recipe']})
        rating = int(data['rating'])
        rated_recipe = {'Ingredients': recipe['Ingredients'],
                        'Instructions': recipe['Instructions'],
                        'Image_Name': recipe['Image_Name'] + '.jpg',
                        'Rating': rating}
        users.update_one({'email': user_email}, {'$set': \
            {f"rated.{recipe['Title']}": rated_recipe}})
        return 'Success', 200
