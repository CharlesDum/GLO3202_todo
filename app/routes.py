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
            lists = [
                        {**todo_list, "_id": str(todo_list["_id"])}
                        for todo_list in mongo.db.lists.find({"owner": current_user.username})
                    ]
            for list in lists:
                list["_id"] = str(list["_id"])
            return render_template("dashboard.html", username = current_user.username, lists=lists)
        return render_template("index.html")
    
    @app.route("/about")
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
            flash("Nom d'utilisateur ou mot de passe incorrect", "error")
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
            flash("Inscription réussie", "success")
            return redirect(url_for("index"))
        
        return render_template("signup.html")
    
    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Déconnexion réussie.", "success")
        return redirect(url_for("index"))

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
                    flash("Le nom de la liste de ne pas être vide", "error")
                    return redirect(url_for("index"))
                
                result = mongo.db.lists.update_one(
                    {"_id": ObjectId(list_id), "owner": current_user.username},
                    {"$set": {"name": new_name}}
                )

                if result.modified_count > 0:
                    flash("Liste mise à jour avec succès", "success")
                else:
                    flash("Impossible de modifier la liste", "error")
            elif action == "delete":
                result = mongo.db.lists.delete_one({"_id": ObjectId(list_id), "owner": current_user.username})

                if result.modified_count > 0:
                    flash("La liste a été supprimée avec succès", "success")
                else:
                    flash("Impossible de supprimer la liste", "error")
        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")
        
        return redirect(url_for("index"))
    
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

            result = mongo.db.lists.update_one(
                {"_id": ObjectId(list_id), "owner": current_user.username},
                {"$push": {"tasks":task}}
            )

            if result.modified_count > 0:
                flash("Tâche ajoutée avec succès", "success")
            else:
                flash("Impossible d'ajouter la tâche", "error")
        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")
        
        return redirect(url_for("index"))
    
    @app.route("/lists/<list_id>/tasks/<task_id>", methods=["POST"])
    @login_required
    def handle_task(list_id, task_id):
        try:
            action = request.form.get("action")
            list_filter = {"_id" : ObjectId(list_id), "owner": current_user.username, "tasks._id": ObjectId(task_id)}

            if action == "update":
                new_description = request.form.get("description")
                completed = request.form.get("completed") == "on"

                result = mongo.db.lists.update_one(
                    list_filter,
                    {"$set": {"tasks.$.description": new_description, "tasks.$.completed": completed}}
                )

                if result.modified_count > 0:
                    flash("Tâche mise à jour avec succès", "success")
                else:
                    flash("Impossible de mettre la tâche à jour", "error")
            
            elif action == "delete":
                result = mongo.db.lists.update_one(
                    {"_id": ObjectId(list_id), "owner": current_user.username},
                    {"$pull": {"tasks": {"_id": ObjectId(task_id)}}}
                )

                if result.modified_count > 0:
                    flash("Tâche supprimée avec succès", "success")
                else:
                    flash("Impossible de supprimer la tâche", "error")
        except Exception as e:
            flash(f"Une erreur est survenue : {str(e)}", "error")

        return redirect(url_for("index"))