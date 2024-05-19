from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chat, User, Movie
from .forms import ChatForm, ChangeInfoForm, SignUpForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    tags = db.session.query(Movie.tag).distinct().all()
    movies = Movie.query.all()
    return render_template('start.html', movies=movies, tags=tags)

@views.route('/moviedetails/<name>')
@login_required
def moviedetails(name):
    # Query the movie by its name
    movieD = Movie.query.filter_by(name=name).first_or_404()  # This will return 404 if no movie is found
    return render_template('views.moviedetails.html', movieD=movieD)

@views.route('/movietag/<tag>')
@login_required
def movietag(tag):
    movieT = Movie.query.filter_by(tag=tag).all()  # Fetch all movies with the given tag
    return render_template('movietag.html', movieT=movieT)

@views.route('/start')
@login_required
def start():
    return render_template('start.html')

@views.route('/search')
@login_required
def search():
    query = request.args.get('query', '')  # Get the query from URL parameters
    if query:
        movieSS = Movie.query.filter(Movie.name.ilike(f'%{query}%')).all()  # Search for movies with names that contain the query
    else:
        movieSS = []
    return render_template('search.html', movieSS=movieSS)  # Assuming you have a template for displaying results

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        form = SignUpForm()
        if not form.validate_on_submit():
            flash('Form validation failed. Please check the errors below and try again.', category='error')
            return render_template('profile.html', user=current_user, form=form)
        
        user_by_email = User.query.filter_by(email=form.email.data).first()
        user_by_username = User.query.filter_by(username=form.username.data).first()
        if user_by_email and user_by_email.id != current_user.id:
            flash('Email already exists. Please use a different email.', category='error')
        elif user_by_username and user_by_username.id != current_user.id:
            flash('Username already exists. Please choose a different username.', category='error')
        else:
            try:
                current_user.email = form.email.data
                current_user.username = form.username.data
                if form.password.data:
                    current_user.password = generate_password_hash(form.password.data, method='sha256')
                db.session.commit()
                flash('Profile updated successfully!', category='success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your profile. Please try again.', category='error')
    
    form = SignUpForm(obj=current_user)
    return render_template('profile.html', user=current_user, form=form)