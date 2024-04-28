from flask import Flask
from flask_login import LoginManager
from .database import db

# Create a login manager object
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify the login view

    # Define the user_loader callback
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular imports
        return User.query.get(int(user_id))

    # Register blueprints
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
