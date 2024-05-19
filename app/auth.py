from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignInForm, SignUpForm
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password.', category='error')
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('start'))        
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
                    password=generate_password_hash(form.password.data, method='sha256')
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully! Welcome to FilmArt.', category='success')
                return redirect(url_for('views.home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again.', category='error')
    
    return render_template('signup.html', form=form)

