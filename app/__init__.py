from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from app.models import User

mongo = PyMongo()

load_dotenv()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv('MONGO_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    mongo.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app