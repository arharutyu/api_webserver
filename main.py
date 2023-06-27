from flask import Flask
from blueprints.cli_bp import cli_bp
from os import environ
from flask_sqlalchemy import SQLAlchemy
from init import db, ma, bcrypt, jwt
from blueprints import registerable_bp

# db = SQLAlchemy()

def setup():
    app = Flask(__name__)

    # app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)

    for bp in registerable_bp:
        app.register_blueprint(bp)

    return app
        
