from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Chat, User
from .forms import ChatForm, ChangeInfoForm
from . import db
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = ChatForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_file = form.img.data
            if image_file:
                filename = secure_filename(image_file.filename)
                img_path = os.path.join('static/uploads', filename)
                image_file.save(img_path)
            else:
                img_path = None

            new_chat = Chat(data=form.data.data, img_path=img_path, user_id=current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            flash('Chat added!', category='success')
            return redirect(url_for('views.home'))

    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return render_template("start.html", user=current_user, form=form, chats=chats)


@views.route('/delete-chat', methods=['POST'])
@login_required
def delete_chat():
    chat_id = request.json.get('chatId')
    chat = Chat.query.get(chat_id)
    if chat and chat.user_id == current_user.id:
        db.session.delete(chat)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Chat not found or unauthorized'}), 404

@views.route('/edit-chat/<int:chat_id>', methods=['GET', 'POST'])
@login_required
def edit_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        flash('Unauthorized action.', category='error')
        return redirect(url_for('views.home'))

    form = ChatForm()
    if request.method == 'POST' and form.validate_on_submit():
        chat.data = form.data.data
        image_file = form.img.data
        if image_file:
            filename = secure_filename(image_file.filename)
            img_path = os.path.join('static/uploads', filename)
            image_file.save(img_path)
            chat.img_path = img_path
        db.session.commit()
        flash('Chat updated!', category='success')
        return redirect(url_for('views.home'))

    form.data.data = chat.data
    return render_template('edit_chat.html', form=form)

@views.route('/change-info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = ChangeInfoForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter_by(email=form.email.data).first()
        user_by_username = User.query.filter_by(username=form.username.data).first()
        
        if user_by_email and user_by_email.id != current_user.id:
            flash('Email already exists.', category='error')
        elif user_by_username and user_by_username.id != current_user.id:
            flash('Username already exists.', category='error')
        else:
            try:
                current_user.username = form.username.data
                current_user.email = form.email.data
                current_user.password = generate_password_hash(form.password.data, method='sha256')
                db.session.commit()
                flash('Information updated successfully!', category='success')
                return redirect(url_for('views.profile'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your information. Please try again.', category='error')    

    return render_template('profile.html', form=form)


@views.route('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts_count = Chat.query.filter_by(user_id=user.id).count()
    followers_count = 0  # Replace with actual follower count logic
    following_count = 0  # Replace with actual following count logic
    posts = Chat.query.filter_by(user_id=user.id).all()
    
    form = ChangeInfoForm()

    return render_template('profile.html', 
                           user=user, 
                           posts_count=posts_count, 
                           followers_count=followers_count, 
                           following_count=following_count,
                           posts=posts,
                           form=form)

""" @flaskApp.route('/')
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
    return render_template('movietag.html', movieT=movieT) """