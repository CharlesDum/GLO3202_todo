from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user, logout_user, login_user
from bson.objectid import ObjectId
from app import mongo, login_manager
from app.models import User
from .forms import SignupForm, LoginForm

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user) if user else None

def register_routes(app):
    # Route vers la page d'accueil [Pas authentifié] ou la page du tableau de bord [Authentifié]
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            lists = [
                        {**todo_list, "_id": str(todo_list["_id"])}
                        for todo_list in mongo.db.lists.find({"owner": current_user.username})
                    ]
            for list in lists:
                list["_id"] = str(list["_id"])
            return render_template("dashboard.html", username=current_user.username, lists=lists)
        return render_template("index.html")
    
    # Route vers la page à propos
    @app.route("/about")
    def about():
        return render_template("about.html")
    
    # Route vers la page de connexion [GET] ou pour connecter un utilisateur [POST]
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data

                user = mongo.db.users.find_one({"username": username})
                if user and user["password"] == password:
                    login_user(User(user))
                    flash("Connexion réussie", "success")
                    return redirect(url_for("index"))
                flash("Nom d'utilisateur ou mot de passe incorrect", "error")

        return render_template("login.html", form=form)

    # Route vers la page d'inscription [GET] ou pour inscrire un nouvel utilisateur [POST]
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        form = SignupForm()
        if request.method == "POST":
            if request.method == "POST":
                if form.validate_on_submit():
                    username = form.username.data
                    password = form.password.data
                    user_id = mongo.db.users.insert_one({"username": username, "password": password}).inserted_id
                    user = mongo.db.users.find_one({"_id": user_id})
                    login_user(User(user))
                    flash("Inscription réussie", "success")
                    return redirect(url_for("index"))
            
        return render_template("signup.html", form=form)
    
    # Route pour déconnecter un utilisateur
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Déconnexion réussie.", "success")
        return redirect(url_for("index"))

    # Route pour créer une liste de tâches
    @app.route("/lists", methods=["POST"])
    @login_required
    def create_list():
        name = request.form.get("name")
        if not name:
            flash("Le nom de la liste est requis", "error")
            return redirect(url_for("index"))
        
        new_list = {
            "name": name,
            "owner": current_user.username,
            "tasks": []
        }
        mongo.db.lists.insert_one(new_list)

        flash("Liste créée avec succès", "success")
        return redirect(url_for("index"))
    
    # Route pour modifier ou supprimer une liste de tâches
    @app.route("/lists/<list_id>", methods=["POST"])
    @login_required
    def handle_list(list_id):
        action = request.form.get("action")

        try:
            list_id = ObjectId(list_id)
        except Exception:
            flash("ID de la liste invalide", "error")
            return redirect(url_for("index"))
        
        try:
            if action == "update":
                new_name = request.form.get("name")
                if not new_name:
                    flash("Le nom de la liste doit contenir au moins un caractère", "error")
                    return redirect(url_for("index"))
                
                mongo.db.lists.update_one(
                    {"_id": ObjectId(list_id), "owner": current_user.username},
                    {"$set": {"name": new_name}}
                )

                flash("Liste mise à jour avec succès", "success")

            elif action == "delete":
                mongo.db.lists.delete_one({"_id": ObjectId(list_id), "owner": current_user.username})

                flash("Liste supprimée avec succès", "success")

        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")
        
        return redirect(url_for("index"))
    
    # Route pour ajouter une tâche
    @app.route("/lists/<list_id>/tasks", methods=["POST"])
    @login_required
    def add_task(list_id):
        try:
            task_description = request.form.get("description")
            if not task_description:
                flash("La description de la tâche est requise", "error")
                return redirect(url_for("index"))
            
            task = {
                "_id": ObjectId(),
                "description": task_description,
                "completed": False
            }

            mongo.db.lists.update_one(
                {"_id": ObjectId(list_id), "owner": current_user.username},
                {"$push": {"tasks":task}}
            )

            flash("Tâche ajoutée avec succès", "success")

        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")
        
        return redirect(url_for("index"))
    
    # Route pour modifier ou Supprimer une tâche
    @app.route("/lists/<list_id>/tasks/<task_id>", methods=["POST"])
    @login_required
    def handle_task(list_id, task_id):
        try:
            action = request.form.get("action")

            list_data = mongo.db.lists.find_one({"_id": ObjectId(list_id), "owner": current_user.username})

            if not list_data:
                abort(403)
            
            task_data = next((t for t in list_data.get("tasks", []) if str(t["_id"]) == task_id), None)

            if not task_data:
                abort(403)

            if action == "update":
                new_description = request.form.get("description")
                completed = request.form.get("completed") == "on"

                if not new_description:
                    flash("La description d'une tâche doit contenir au moins un caractère", "error")
                    return redirect(url_for("index"))

                mongo.db.lists.update_one(
                    {"_id": ObjectId(list_id), "owner": current_user.username, "tasks._id": ObjectId(task_id)},
                    {"$set": {"tasks.$.description": new_description, "tasks.$.completed": completed}}
                )

                flash("Tâche mise à jour avec succès", "success")
            
            elif action == "delete":
                mongo.db.lists.update_one(
                    {"_id": ObjectId(list_id), "owner": current_user.username},
                    {"$pull": {"tasks": {"_id": ObjectId(task_id)}}}
                )

                flash("Tâche supprimée avec succès", "success")

        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")

        return redirect(url_for("index"))