from flask import render_template
from app import flaskApp
import SQLAIchemy

@flaskApp.route("/")
@flaskApp.route('/index')

def index():
    categories = ['HomePage', 'Action', 'Anime', 'Comedy', 'Romance', 'Horror', 'Sci-Fi', 'Crime', 'Classics', 'Thriller', 'Document', 'Posts']

    movie_data=SQLAIchemy.get_movie_data()

    movies=[{'title' : movie['title'], 'image_url': movie["image_url"]}for movie in movie_data] 

    return render_template('test2.html',categories=categories, movies=movies)



if __name__ == '__main__':
    flaskApp.run(debug=True)