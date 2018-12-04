#
#   Imports
#
from settings import *
from flask import Flask
from flask_mongoengine import MongoEngine

#
#   Flask server
#
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': DATABASE_NAME,
    'host': DATABASE_URI
}
app.config['SECRET_KEY'] = CSRF_SECRET_KEY

#
#   MongoDB engine
#
db = MongoEngine(app)