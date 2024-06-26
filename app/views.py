from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chat, User, Movie
from .forms import ChatForm, ChangeUsernameEmailForm, SignUpForm, ChangePasswordForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/start')
@views.route('/')
@login_required
def home():
    tags = db.session.query(Movie.tag).distinct().all()
    movies = Movie.query.all()
    return render_template('start.html', movies=movies, tags=tags)

@views.route('/movie/<name>', methods=['GET'])
def moviedetails(name):
    movieD = Movie.query.filter_by(name=name).first_or_404()
    chats = Chat.query.filter_by(movie_name=name).all()
    return render_template('moviedetails.html', movieD=movieD, chats=chats)

@views.route('/submit_comment/<movie_name>', methods=['POST'])
@login_required
def submit_comment(movie_name):
    movie = Movie.query.filter_by(name=movie_name).first_or_404()
    comment_data = request.form.get('comment')
    new_chat = Chat(data=comment_data, user_id=current_user.id, movie_name=movie.name)
    db.session.add(new_chat)
    db.session.commit()
    flash('Your comment has been added!', category='success')
    return redirect(url_for('views.moviedetails', name=movie.name))

@views.route('/delete_comment/<int:chat_id>', methods=['POST'])
@login_required
def delete_comment(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        flash('You are not authorized to delete this comment.', category='error')
        return redirect(url_for('views.moviedetails', name=chat.movie_name))
    db.session.delete(chat)
    db.session.commit()
    flash('Your comment has been deleted!', category='success')
    return redirect(url_for('views.moviedetails', name=chat.movie_name))

@views.route('/like_comment/<int:chat_id>', methods=['POST'])
@login_required
def like_comment(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    user = User.query.get(current_user.id)
    
    if chat_id in user.liked_chats:
        chat.likes -= 1
        user.liked_chats.remove(chat_id)
        flash(f'Removed like from chat {chat_id}', category='info')
    else:
        if chat_id in user.disliked_chats:
            chat.dislikes -= 1
            user.disliked_chats.remove(chat_id)
        chat.likes += 1
        user.liked_chats.append(chat_id)
        flash(f'Liked chat {chat_id}', category='info')
    db.session.commit()

    return redirect(url_for('views.moviedetails', name=chat.movie_name))

@views.route('/dislike_comment/<int:chat_id>', methods=['POST'])
@login_required
def dislike_comment(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat_id in current_user.disliked_chats:
        current_user.disliked_chats.remove(chat_id)
        chat.dislikes -= 1
    else:
        if chat_id in current_user.liked_chats:
            current_user.liked_chats.remove(chat_id)
            chat.likes -= 1
        current_user.disliked_chats.append(chat_id)
        chat.dislikes += 1
    db.session.commit()
    return redirect(url_for('views.moviedetails', name=chat.movie_name))

@views.route('/movietag/<tag>')
@login_required
def movietag(tag):
    movieT = Movie.query.filter_by(tag=tag).all()  # Fetch all movies with the given tag
    tag = tag.capitalize()
    return render_template('movietag.html', movieT=movieT, tag=tag)

@views.route('/search')
@login_required
def search():
    query = request.args.get('query', '')  # Get the query from URL parameters
    if query:
        movieSS = Movie.query.filter(Movie.name.ilike(f'%{query}%')).all()  # Search for movies with names that contain the query
    else:
        movieSS = []
    return render_template('search.html', movieSS=movieSS)  # Assuming you have a template for displaying results

@views.route('/profile', methods=['GET'])
@login_required
def profile():
    name_email_form = ChangeUsernameEmailForm(obj=current_user)
    pw_form = ChangePasswordForm()
    liked_chats = Chat.query.filter(Chat.id.in_(current_user.liked_chats)).all() if current_user.liked_chats else []
    disliked_chats = Chat.query.filter(Chat.id.in_(current_user.disliked_chats)).all() if current_user.disliked_chats else []

    return render_template('profile.html', user=current_user, name_email_form=name_email_form, pw_form=pw_form, liked_chats=liked_chats, disliked_chats=disliked_chats)

@views.route('/profile-namechange', methods=['POST'])
@login_required
def update_name_email():
    form = ChangeUsernameEmailForm()
    if form.validate_on_submit():
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
                db.session.commit()
                flash('Profile updated successfully!', category='success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your profile. Please try again.', category='error')
    else:
        flash('Form validation failed. Please check the errors below and try again.', category='error')

    return redirect(url_for('views.profile'))

@views.route('/profile-pwchange', methods=['POST'])
@login_required
def update_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            current_user.password = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password updated successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your password. Please try again.', category='error')
    else:
        flash('Form validation failed. Please check the errors below and try again.', category='error')

    return redirect(url_for('views.profile'))
