from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from application import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), unique=False, default='USER')
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"User('{ self.id }', '{ self.username }', '{ self.password }')"

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)