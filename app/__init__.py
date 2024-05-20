import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate, init as flask_migrate_init, migrate as flask_migrate_migrate, upgrade as flask_migrate_upgrade
from .config import Config, DevelopmentConfig
from flask_wtf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()
DB_NAME = 'app.db'

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    else:
        app.config.from_object(Config)
    
    
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Chat, Movie  # Import your models

    login_manager = LoginManager()
    login_manager.login_view = 'auth.sign_in'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        initialize_or_upgrade_database()

    return app

def initialize_or_upgrade_database():
    """Initialize the migration repository and create the database if it doesn't exist, otherwise upgrade"""
    migrations_dir = os.path.join(os.path.dirname(__file__), '../migrations')

    if not os.path.exists(migrations_dir):
        print("Initializing migration repository...")
        flask_migrate_init(directory=migrations_dir)
    
    if not os.path.exists(DB_NAME):
        print("Generating initial migration...")
        flask_migrate_migrate(message="Initial migration", directory=migrations_dir)
        print("Upgrading database schema...")
        flask_migrate_upgrade(directory=migrations_dir)
        print('Created Database!')
    else:
        upgrade_database()

def upgrade_database():
    """Apply any pending migrations automatically"""
    try:
        print("Upgrading database schema...")
        migrations_dir = os.path.join(os.path.dirname(__file__), '../migrations')
        flask_migrate_upgrade(directory=migrations_dir)
        print("Database schema is up to date.")
    except Exception as e:
        print(f"An error occurred during database upgrade: {e}")
