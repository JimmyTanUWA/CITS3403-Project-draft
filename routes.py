from app import flaskApp, db
from flask import render_template, redirect, flash, url_for, request, jsonify
from app.models import movie, user
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

@flaskApp.route('/search')
def search():
    query = request.args.get('query', '')  # Get the query from URL parameters
    if query:
        movieSS = movie.query.filter(movie.name.ilike(f'%{query}%')).all()  # Search for movies with names that contain the query
    else:
        movieSS = []
    return render_template('search.html', movieSS=movieSS)  # Assuming you have a template for displaying results

@flaskApp.route('/profile')
def profile():
    user = user.query.first()
    return render_template('profile.html', user=user)






