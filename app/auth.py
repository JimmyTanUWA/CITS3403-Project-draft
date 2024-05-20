from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignInForm, SignUpForm, ChangeInfoForm
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.start'))
    
    form = SignUpForm()
    
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Form validation failed. Please check the errors below and try again.', category='error')
            return render_template('signup.html', form=form)
        
        user_by_email = User.query.filter_by(email=form.email.data).first()
        user_by_username = User.query.filter_by(username=form.username.data).first()
        
        if user_by_email:
            flash('Email already exists. Please use a different email.', category='error')
        elif user_by_username:
            flash('Username already exists. Please choose a different username.', category='error')
        else:
            try:
                new_user = User(
                    email=form.email.data,
                    username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    liked_chats=[],  # Initialize liked_chats as an empty list
                    disliked_chats=[]  # Initialize disliked_chats as an empty list
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully! Welcome to FilmArt.', category='success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash(str(e), category='error')
    
    return render_template('signup.html', form=form)

@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:     
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect', category='error')
    return render_template('signin.html', form=form)

@auth.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('auth.sign_in'))

@auth.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = ChangeInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your profile has been updated!', category='success')
        return redirect(url_for('views.profile'))
    return render_template('profile.html', user=current_user, form=form)


@auth.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    file = request.files.get('profile_pic')
    if not file or file.filename == '':
        flash('No selected file', category='error')
        return redirect(url_for('views.profile'))
    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.static_folder, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        # Replace backslashes with forward slashes
        relative_file_path = os.path.join('uploads', filename).replace('\\', '/')
        current_user.profile_pic = relative_file_path
        db.session.commit()
        flash('Profile picture updated!', category='success')
    else:
        flash('Invalid file type', category='error')
    return redirect(url_for('views.profile'))


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



