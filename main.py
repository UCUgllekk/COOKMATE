'''app.py'''
from flask import render_template, request, jsonify
from flask.views import MethodView

from __init__ import app, ingredients
from login import LoginView, LogoutView, SignUpView
from user_profile import LikedView, RatedView, RateView
from ingredients import StoreDataView, StoreLikedRecipesView, RecipeView, \
                                                IngredientsView, TinderView

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
        results = ingredients.find({"name": {"$regex": query.strip()}})
        suggestions = sorted([result['name'] for result in results], key=len)
        return jsonify(suggestions)

app.add_url_rule('/', view_func=MainView.as_view('main_page'))
app.add_url_rule('/ingredients', view_func=IngredientsView.as_view('ingredients'))
app.add_url_rule('/login', view_func=LoginView.as_view('log_in'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/sign_up', view_func=SignUpView.as_view('sign_up'))
app.add_url_rule('/search', view_func=SearchView.as_view('search_view'))
app.add_url_rule('/tinder', view_func=TinderView.as_view('tinder'))
app.add_url_rule('/liked', view_func=LikedView.as_view('liked'))
app.add_url_rule('/store_data', view_func=StoreDataView.as_view('store_data'))
app.add_url_rule('/store_liked_recipes', view_func=StoreLikedRecipesView.as_view('store_liked_recipes'))
app.add_url_rule('/rated', view_func=RatedView.as_view('rated'))
app.add_url_rule('/rate', view_func=RateView.as_view('rate'))
app.add_url_rule('/recipe/<recipe_id>/', view_func=RecipeView.as_view('recipe'))

if __name__ == '__main__':
    app.run(debug=True)
