from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
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
        DataRequired(message="Le nom d'utilisateur est requis")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired("Le mot de passe est requis")
    ])
    submit = SubmitField("Se connecter")