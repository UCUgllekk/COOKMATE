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
            print(users.user_email.liked)
            liked = user['liked']
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

    def post(self):
        '''Like'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            liked = user['liked']
            if request.form.get('knopka').startswith("delete:"):
                recipe_title = request.form.get('knopka')[7:]
                if recipe_title not in liked:
                    return render_template('liked.html', recipes = liked)
                users.update_one({'email': user_email}
                        , {'$unset': {f'liked.{recipe_title}': liked[recipe_title]}})
                if recipe_title in user['rated']:
                    users.update_one({'email': user_email}
                        , {'$unset': {f'rated.{recipe_title}': user['rated'][recipe_title]}})
                user = users.find_one({"email": user_email})
                liked = user['liked']
                return render_template('liked.html', recipes = liked)
            sort_type = request.form.get('knopka')
            if sort_type == 'name':
                liked = dict(sorted(liked.items()))
            elif sort_type == 'amount':
                liked = dict(sorted(liked.items(), key=lambda x: len(x[1]['Ingredients'].split("; "))))
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

class RatedView(MethodView):
    '''View Recipes'''
    def get(self):
        '''Recipes'''
        session['sort_type'] = ""
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
            rated = user['rated']
            if request.form.get('knopka').startswith("delete:"):
                recipe_title = request.form.get('knopka')[7:]
                if recipe_title not in rated or recipe_title not in user['liked']:
                    return render_template('liked.html', recipes = rated)
                users.update_one({'email': user_email}
                            , {'$set': {f"liked.{recipe_title}.Rating": 0}})
                users.update_one({'email': user_email}
                            , {'$unset': {f'rated.{recipe_title}': user['rated'][recipe_title]}})
                user = users.find_one({"email": user_email})
                rated = user['rated']
                return render_template('rated.html', recipes = rated)
            sort_type = request.form.get('knopka')
            print(session['sort_type'])
            if sort_type == session['sort_type']:
                sort_type = ""
            elif sort_type == '1 star':
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
            session['sort_type'] = sort_type
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
            {f"liked.{recipe['Title']}.Rating": rating}})
        users.update_one({'email': user_email}, {'$set' if rating else '$unset': \
            {f"rated.{recipe['Title']}": rated_recipe}})
        return 'Success', 200
