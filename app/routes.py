from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from bson.objectid import ObjectId
from app import mongo, login_manager
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user) if user else None

def register_routes(app):
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return render_template("dashboard.html", username = current_user.username)
        return render_template("index.html")
    
    @app.route("/about")
    @login_required
    def about():
        return render_template("about.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = mongo.db.users.find_one({"username": username})
            if user and user["password"] == password:
                login_user(User(user))
                flash("Connexion réussie.", "success")
                return redirect(url_for("index"))
            flash("Nom d'utilisateur ou mot de passe incorrect.", "error")
        return render_template("login.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            existing_user = mongo.db.users.find_one({"username": username})
            if existing_user:
                flash("Nom d'utilisateur existe déjà", "error")
                return redirect(url_for("signup"))

            user_id = mongo.db.users.insert_one({
                "username": username,
                "password": password
            }).inserted_id

            user = mongo.db.users.find_one({"_id": user_id})
            login_user(User(user))
            flash("Inscription réussie.", "success")
            return redirect(url_for("index"))
        
        return render_template("signup.html")
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Déconnexion réussie.", "success")
        return redirect(url_for("index"))