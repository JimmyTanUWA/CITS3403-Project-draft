from typing import List
from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_sqlalchemy import SQLAlchemy
import random

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
    
class user(db.Model):
    username = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'

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


