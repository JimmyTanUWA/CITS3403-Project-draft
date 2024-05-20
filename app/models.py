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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    chats = db.relationship('Chat', backref='user', lazy=True)
    profile_pic = db.Column(db.String(120), nullable=True)
    liked_chats = db.Column(db.PickleType, default=[])
    disliked_chats = db.Column(db.PickleType, default=[])

    def get_id(self):
        return str(self.id)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f'<Reply {self.id} {self.data}>'

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    img_path = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_name = db.Column(db.String(100), db.ForeignKey('movies.name'), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)


    def __repr__(self) -> str:
        return f'<Chat {self.id} {self.data}>'
