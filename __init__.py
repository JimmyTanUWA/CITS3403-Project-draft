from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from os import path, makedirs

db = SQLAlchemy()
DB_NAME = 'app.db'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Chat

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        initialize_or_upgrade_database()

    return app

def initialize_or_upgrade_database():
    """Initialize the migration repository and create the database if it doesn't exist, otherwise upgrade"""
    if not path.exists('app/' + DB_NAME):
        makedirs(path.dirname('app/' + DB_NAME), exist_ok=True)
        print("Initializing migration repository...")
        from flask_migrate import init as flask_migrate_init
        flask_migrate_init()
        print("Generating initial migration...")
        from flask_migrate import migrate as flask_migrate_migrate
        flask_migrate_migrate(message="Initial migration")
        print("Upgrading database schema...")
        from flask_migrate import upgrade as flask_migrate_upgrade
        flask_migrate_upgrade()
        print('Created Database!')
    else:
        upgrade_database()

def upgrade_database():
    """Apply any pending migrations automatically"""
    try:
        print("Upgrading database schema...")
        from flask_migrate import upgrade as flask_migrate_upgrade
        flask_migrate_upgrade()
        print("Database schema is up to date.")
    except Exception as e:
        print(f"An error occurred during database upgrade: {e}")

