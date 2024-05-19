from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from .models import User
from flask_login import current_user

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(), 
        Length(min=6, message='Password should be at least 6 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    signup_submit = SubmitField('Confirm Sign-Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ChatForm(FlaskForm):
    data = StringField('Chat Content', validators=[InputRequired(), Length(min=1, max=1000)])
    img = FileField('Upload Image')
    submit = SubmitField('Add Chat')


class ChangeInfoForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[
        InputRequired(), 
        Length(min=6, message='Password should be at least 6 characters long.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Confirm Change')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered.')
            
            #TODO edit profile
            #TODO ability to comment on movies
            #TODO add some bottom page functionality
            #TODO change all inconsistent naming