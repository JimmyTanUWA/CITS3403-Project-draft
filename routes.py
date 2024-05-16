from app import flaskApp, db
from flask import render_template, redirect, flash, url_for
from app.models import movie
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

@flaskApp.route('/')
def index():
    tags = db.session.query(movie.tag).distinct().all()
    movies = movie.query.all()
    return render_template('original.html', movies=movies, tags=tags)

@flaskApp.route('/moviedetails/<name>')
def moviedetails(name):
    # Query the movie by its name
    movieD = movie.query.filter_by(name=name).first_or_404()  # This will return 404 if no movie is found
    return render_template('moviedetails.html', movieD=movieD)

@flaskApp.route('/movietag/<tag>')
def movietag(tag):
    movieT = movie.query.filter_by(tag=tag).all()  # Fetch all movies with the given tag
    return render_template('movietag.html', movieT=movieT)

@flaskApp.route('/start')
def start():
    return render_template('start.html')

@flaskApp.route('/signup')
def signup():
    return render_template('signup.html')

@flaskApp.route('/signin')
def signin():
    return render_template('signin.html')


