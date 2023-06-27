from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints import registerable_bp

def setup():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = "Mushu is the Best"
    
    # environ.get('JWT_KEY')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    for bp in registerable_bp:
        app.register_blueprint(bp)

    return app
        
