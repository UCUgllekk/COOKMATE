
# class LoginView(MethodView):
#     '''LoginView'''
#     def get(self):
#         '''LoginPage'''
#         message = ''
#         print(session)
#         if 'email' in session:
#             return render_template('liked.html')
#         return render_template('login.html', message=message)

#     def post(self):
#         '''Login'''
#         email = request.form.get('email')
#         password = request.form.get('password')
#         user_found = records.find_one({'email': email})
#         if user_found:
#             user_val = user_found['email']
#             passwordcheck = user_found['password']
#             if check_password_hash(passwordcheck, password):
#                 session['email'] = user_val
#                 return render_template('liked.html')
#             if 'email' in session:
#                 return render_template('liked.html')
#             message = "Wrong Password!"
#             return render_template('login.html', message=message)
#         message = "User does not exist!"
#         return render_template('login.html', message=message)


class StoreDataView(MethodView):
    def get(self):
        data = request.data
        data = json.loads(data)
        # Now data is a Python list
        # Store it in the session
        print(f"{data=}")
        session['selected_ingredients'] = data
        found_recipes = find_with_majority_ingredients(data, 0.5)
        return '', 200  # Return found_recipes in the response

# class StoreDataView(MethodView):
#     def post(self):
#         data = request.data
#         data = json.loads(data)
#         print(session)
#         session['selected_ingredients'] = data
#         print(session)
#         found_recipes = find_with_majority_ingredients(data, 0.5)
#         return jsonify(found_recipes), 200

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
app.add_url_rule('/store_data', view_func=StoreDataView.as_view('store_data'))
