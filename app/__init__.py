from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
import os

mongo = PyMongo()

login_manager = LoginManager()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
    ) 

def create_app():
    app = Flask(__name__)

    app.config.update(
        SESSION_COOKIE_SAMESITE='Strict',
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
    )
    
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


    if not app.config["MONGO_URI"] or not app.config["SECRET_KEY"]:
        raise ValueError("Les variables d'environnement MONGO_URI et SECRET_KEY ne sont pas définies")

    mongo.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = "login"

    csp = {
        "default-src" : ['\'self\''],
        "script-src" : ['\'self\''],
        "img-src" : ['\'self\'', 'data:'],
        "font-src": ['\'self\''],
        "connect-src": ['\'self\'']
    }

    Talisman(app, content_security_policy=csp)

    return app