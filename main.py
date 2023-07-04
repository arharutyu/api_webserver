from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints import registerable_bp
from marshmallow import ValidationError

def setup():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = "Mushu is the Best"
    
    # environ.get('JWT_KEY')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    @app.errorhandler(404)
    def bad_request(err):
        return {'error': str(err)}, 404
            
    @app.errorhandler(405)
    def method_not_allowed(err):
        return {'error': str(err)}, 405
    
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.__dict__['messages']}, 400

    for bp in registerable_bp:
        app.register_blueprint(bp)

    return app
        
