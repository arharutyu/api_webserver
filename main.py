from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints import registerable_bp
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

def setup():
    # Create Flask application
    app = Flask(__name__)
    # Configure app using information from env variables
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
    # Initiate SQLAlchemy, Marshmallow, JWT Authorization, and Bcrypt instances
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    # Error handling for relevant codes to return in JSON format
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404
            
    @app.errorhandler(405)
    def method_not_allowed(err):
        return {'error': str(err)}, 405
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.__dict__['messages']}, 400
    
    @app.errorhandler(IntegrityError)
    def validation_error(err):
        return {'error': f"Integrity Error details: {err.__dict__['orig']}"}, 404
    # Register blueprints for use 
    for bp in registerable_bp:
        app.register_blueprint(bp)

    return app
        
