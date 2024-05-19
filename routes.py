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

@flaskApp.route('/start')
def start():
    return render_template('start.html')

@flaskApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # In a real app, you should hash this password!

        # Create a new user instance and add it to the database
        new_user = user(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('signin'))  # Redirect to the login page after successful signup
    return render_template('signup.html')

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

#@flaskApp.route('/upload', methods=['POST'])
#def upload():
    #if 'file' not in request.files:
        ##file = request.files['file']
    #if file.filename == '':
        #return redirect(request.url)
    #if file:
        #filename = secure_filename(file.filename)
        #file.save(os.path.join(flaskApp.config['UPLOAD_FOLDER'], filename))
        ##user.profile_image = filename
        ##return redirect(url_for('profile'))




