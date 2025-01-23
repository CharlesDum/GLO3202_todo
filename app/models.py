from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password = user_data["password"]
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True