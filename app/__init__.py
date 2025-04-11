from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

# Create a Flask application instance
myapp_obj = Flask(__name__)

# Set the base directory path for the application (where this file is located)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration settings for the Flask application
myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',  # Secret key for session management and CSRF protection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),  # SQLite database URI (app.db will be in the base directory)
)

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(myapp_obj)

# Initialize the LoginManager for managing user authentication
login = LoginManager()
login.init_app(myapp_obj)  # Link the LoginManager with the Flask app
login.login_view = "login"  # If an unauthorized user tries to access a protected route, they will be redirected to the 'login' route
login.login_message = "You need to log in to access this page."  # Custom message that will be shown to unauthorized users

# Import routes and models after app initialization to avoid circular imports
from app import routes, models
from app.models import User

# Define the user loader function that Flask-Login will use to get the user object
@login.user_loader
def load_user(id):
    return User.query.get(int(id))  # Fetch the user by ID from the database