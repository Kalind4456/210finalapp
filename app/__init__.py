from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create the SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the Flask app, including database URI, secret key, etc.
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)

    # Import and register Blueprints
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import the User model for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
