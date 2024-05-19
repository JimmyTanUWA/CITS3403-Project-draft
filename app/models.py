from typing import List
from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movies'
    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(1000), nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    release_date = db.Column(db.String(20), nullable=False)
    runtime = db.Column(db.String(20), nullable=False)
    plot = db.Column(db.String(1000), nullable=False)
    chats = db.relationship('Chat', backref='movie', lazy=True, foreign_keys='Chat.movie_name')  # Explicit foreign_keys

    def __repr__(self) -> str:
        return f'<Movie {self.name} {self.tag} {self.address} {self.rating} {self.release_date} {self.runtime} {self.plot}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(150), unique=True, nullable=False)  # Unique email address
    password = db.Column(db.String(150), nullable=False)  # User's password
    username = db.Column(db.String(150), nullable=False)  # User's username
    chats = db.relationship('Chat', backref='user', lazy=True, foreign_keys='Chat.user_id')  # Explicit foreign_keys

    def get_id(self):
        return str(self.id)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the chat
    data = db.Column(db.String(1000))  # Text content of the chat
    img_path = db.Column(db.String(100), nullable=True)  # Optional image path
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of chat creation
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    movie_name = db.Column(db.String(100), db.ForeignKey('movies.name'), nullable=False)  # Foreign key to Movie

    def __repr__(self) -> str:
        return f'<Chat {self.id} {self.data}>'
