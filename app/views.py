from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chat, User, Movie
from .forms import ChatForm, ChangeInfoForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/')
def home():
    tags = db.session.query(Movie.tag).distinct().all()
    movies = Movie.query.all()
    return render_template('start.html', movies=movies, tags=tags)

@views.route('/moviedetails/<name>')
def moviedetails(name):
    # Query the movie by its name
    movieD = Movie.query.filter_by(name=name).first_or_404()  # This will return 404 if no movie is found
    return render_template('views.moviedetails.html', movieD=movieD)

@views.route('/movietag/<tag>')
def movietag(tag):
    movieT = Movie.query.filter_by(tag=tag).all()  # Fetch all movies with the given tag
    return render_template('movietag.html', movieT=movieT)

@views.route('/start')
def start():
    return render_template('start.html')

@views.route('/search')
def search():
    query = request.args.get('query', '')  # Get the query from URL parameters
    if query:
        movieSS = Movie.query.filter(Movie.name.ilike(f'%{query}%')).all()  # Search for movies with names that contain the query
    else:
        movieSS = []
    return render_template('search.html', movieSS=movieSS)  # Assuming you have a template for displaying results

@views.route('/profile')
def profile():
    user = User.query.first()
    return render_template('profile.html', user=user)