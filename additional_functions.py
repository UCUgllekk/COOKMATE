'''validate functions for program'''
import re
from __init__ import dbrecipes

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

def validate_email(email:str):
    '''email'''
    return bool(re.fullmatch(r"^(?!\.)[a-z!#$%&'*+\-/=?^_`{|}~]+(?:\.[a-z!#$%&'*+\-/=?^_`"+\
        r"{|}~]{1,64})*@[a-z]{1,255}(\.(gmail|ucu|com|org|edu|gov|net|ua))+", email))

def find_with_majority_ingredients(ingredient_list, amount: float):
    '''Find recipes by ingredients'''
    all_docs = dbrecipes.find({}, {"Cleaned_Ingredients": 1, "Image_Name": 1, \
        "Title": 1, "Ingredients": 1, 'Instructions': 1})
    matching_docs = []
    for doc in all_docs:
        doc_ingredients = doc['Cleaned_Ingredients'][2:-2].split("', '")
        common_ingredients = set(doc_ingredients) & set(ingredient_list)
        if len(common_ingredients) / len(doc_ingredients) > amount:
            if all(key_name in doc for key_name in ['Image_Name', \
                'Title', 'Ingredients', 'Instructions']):
                matching_docs.append(doc['Image_Name'])
                matching_docs.append(doc['Title'])
                matching_docs.append(doc['Ingredients'])
                matching_docs.append(doc['Instructions'])
    return matching_docs
