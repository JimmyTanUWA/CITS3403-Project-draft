from typing import List
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import random
from datetime import datetime

class movie(db.Model):
    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(1000), nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    release_date = db.Column(db.String(20),nullable=False)
    runtime = db.Column(db.String(20),nullable=False)
    plot = db.Column(db.String(1000),nullable=False)

    def __repr__(self) -> str:
        return f'moviedetails {self.name} {self.tag} {self.address} {self.rating} {self.release_date} {self.runtime} {self.plot}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(150), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(150), nullable=False)  # User's password
    username = db.Column(db.String(150), nullable=False)  # User's username

    def get_id(self):
        return str(self.id)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the chat
    data = db.Column(db.String(1000))  # Text content of the chat
    img_path = db.Column(db.String(100), nullable=True)  # Optional image path
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of chat creation
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    user = db.relationship('User', backref=db.backref('chats', lazy=True))  # Relationship to User

    def __repr__(self):
        return f'<Chat {self.id}>'

#class User(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(100), nullable=False)
    #password = db.Column(db.String(100), nullable=False)

#def generate_unique_id():
    #while True:
        #potential_id = random.randint(100000000, 999999999)
        #if not User.query.filter_by(id=potential_id).first():
            #return potential_id

#class Comment(db.Model):
    #user_name = db.Column(db.String(20), db.ForeignKey('user.name'), nullable=False)
    #content = db.Column(db.Text, nullable=False)
    #date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    #user = db.relationship('User', backref=db.backref('comments', lazy=True))

