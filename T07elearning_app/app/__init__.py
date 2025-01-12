# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, migrate, mail, socketio, compress
from app.models import User  # Import the User model
from flask_login import LoginManager

# Initialize the login manager
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    socketio.init_app(app)
    compress.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.lecturer import bp as lecturer_bp
    app.register_blueprint(lecturer_bp, url_prefix='/lecturer')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Import models
    from app import models

    @app.cli.command("seed")
    def seed():
        """Insert sample data into the database."""
        from populate_db import populate
        populate()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
