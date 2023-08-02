from flask import Flask
from .extensions import db, migrate
from dotenv import find_dotenv, load_dotenv

import os

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from .models import Wine, Notes

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app