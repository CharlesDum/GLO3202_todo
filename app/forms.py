from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app import mongo

# Formulaire d'inscription
class SignupForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(message="Le nom d'utilisateur est requis"),
        Length(min=3, max=20, message="Le nom d'utilisateur doit comporter entre 3 et 20 caractères")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message="Le mot de passe est requis"),
        Length(min=6, message="Le mot de passe doit contenir au moins 10 caractères")
    ])
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = mongo.db.users.find_one({"username": username.data})
        if user:
            raise ValidationError("Ce nom d'utilisateur est déjà pris")

# Formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Nom  d\'utilisateur', validators=[
        DataRequired("Le nom d'utilisateur est requis")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired("Le mot de passe est requis")
    ])
    submit = SubmitField("Se connecter")

# Formulaire pour créer une liste
class CreateListForm(FlaskForm):
    name = StringField('Nom de la liste', validators=[
        DataRequired("Le nom de la liste est requis")
        ])

# Formulaire pour gérer les listes existantes
class ListForm(FlaskForm):
    name = StringField('Nom de la liste', validators=[
        DataRequired("Le nom de la liste est requis")
        ])
    update = SubmitField('Appliquer')
    delete = SubmitField('Supprimer')

# Formulaire pour gérer les tâches associées à une liste
class TaskForm(FlaskForm):
    description = StringField('Description', validators=[
        DataRequired("La description de la tâche est requise")
        ])
    completed = BooleanField('Terminée')
    update = SubmitField('Appliquer')
    delete = SubmitField('Supprimer')