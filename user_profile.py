'''user profile'''
import json
from flask import render_template, session, request, redirect, url_for
from flask.views import MethodView
from __init__ import users, dbrecipes

class LikedView(MethodView):
    '''Liked'''
    def get(self):
        '''open liked'''
        session["sort_type"] = ""
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            liked = user['liked']
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

    def post(self):
        '''Like'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            liked = user['liked']
            deleting = False
            if request.form.get('knopka').startswith("Delete all liked without"):
                # for title, recipe_info in liked.items():
                #     if not recipe_info["Rating"]:
                #         users.update_one({'email': user_email}, {'$unset': {f'liked.{title}': recipe_info}})
                users.update_one({"email": user_email}, {"$set": {"liked": {}}})
                rated = user["rated"]
                tuple_rated = tuple(rated.items())
                for i in range(0, len(rated), 50):
                    users.update_many({"email": user_email}, [{'$set': {f'liked.{meal[0]}': meal[1]}} for meal in tuple_rated[i*50:(i + 1) * 50]])
                return redirect(url_for("liked"))
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
                deleting = True
            if not deleting:
                sort_type = request.form.get('knopka')
            else:
                sort_type = session["sort_type"] if "sort_type" in session else ""
            if sort_type == 'name':
                liked = dict(sorted(liked.items()))
            elif sort_type == 'amount':
                liked = dict(sorted(liked.items(), key=lambda x: len(x[1]['Ingredients'].split("; "))))
            session['sort_type'] = sort_type
            return render_template('liked.html', recipes = liked)
        return render_template('login.html')

class RatedView(MethodView):
    '''View Recipes'''
    def get(self):
        '''Recipes'''
        if "sort_type" not in session:
            session["sort_type"] = ""
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            rated_recipes = user['rated']
            if session["sort_type"] and session["sort_type"][0].isnumeric():
                rated_recipes = {name:parameters for name,parameters in rated_recipes.items() \
                    if parameters['Rating'] == int(session["sort_type"][0])}
            return render_template('rated.html', recipes=rated_recipes, filtered=len(user['rated']) > len(rated_recipes))
        return render_template('login.html')

    def post(self):
        '''Like'''
        if 'email' in session:
            user_email = session.get('email')
            user = users.find_one({"email": user_email})
            deleting = False
            rated = user['rated']
            if request.form.get('knopka').startswith("delete:"):
                recipe_title = request.form.get('knopka')[7:]
                users.update_one({'email': user_email}
                            , {'$unset': {f'rated.{recipe_title}': user['rated'][recipe_title]}})
                if recipe_title in user['liked']:
                    users.update_one({'email': user_email}
                            , {'$set': {f"liked.{recipe_title}.Rating": 0}})
                user = users.find_one({"email": user_email})
                rated = user['rated']
                deleting = True
            if not deleting:
                sort_type = request.form.get('knopka')
                if sort_type == session['sort_type'] or not rated:
                    session['sort_type'] = ""
                    return redirect(url_for("rated"))
            else:
                sort_type = session["sort_type"] if "sort_type" in session and rated else ""
            session['sort_type'] = sort_type
            return redirect(url_for("rated"))
        return render_template('login.html', filtered=False)


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
