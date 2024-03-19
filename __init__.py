'''setting up for program'''
import secrets
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://pavlosiukpn:U221Bd9n@cookma"+\
    "tecluster.uqlmdxd.mongodb.net/python_project"

secret_key = secrets.token_hex(16)
app.secret_key = secret_key

mongo = PyMongo(app)
users = mongo.db.users
dbrecipes = mongo.db.recipes
ingredients = mongo.db.ingredients
