from stronka import db, login_manager
from stronka import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    verification_token = db.Column(db.String(32))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode(
            "utf-8"
        )

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class SearchHistory(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    items = db.Column(db.String(length=100), nullable=False)
    search_date = db.Column(db.DateTime, nullable=False, default=datetime.date.today())
