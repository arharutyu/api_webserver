from flask import Blueprint, request, abort
from datetime import timedelta
from models.user import User
from schemas.user_schema import UserSchema, user_schema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, access_required
from marshmallow.exceptions import ValidationError

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    admin_required()
    try:
        # Parse, sanitize and validate the incoming JSON data
        # via the schema
        errors = user_schema.validate(request.json)
        if errors:
           return {'error': errors}, 409
        user_info = user_schema.load(request.json)
        # Create a new User model instance with the schema data
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            is_admin=user_info['is_admin'],
            access=user_info['access']
        )

        # Add and commit the new user
        db.session.add(user)
        db.session.commit()

        # Return the new user, excluding the password
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409



@user_bp.route('/users')
@jwt_required()
def all_users():
    access_required()
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@user_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  user_info = UserSchema().load(request.json)
  if user:
    admin_required()
    user.first_name = user_info.get('first_name', user.first_name)
    user.last_name = user_info.get('last_name', user.last_name)
    user.email = user_info.get('email', user.email)
    user.password = bcrypt.generate_password_hash(user_info.get('password', user.password)).decode('utf-8')
    user.is_admin = user_info.get('is_admin', user.is_admin)
    user.access = user_info.get('access', user.access)

    db.session.commit()
    return UserSchema(exclude=['password']).dump(user), 201
  
  else:
    return {'error': 'User not found'}, 404
  
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
  admin_required()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if user:
    db.session.delete(user)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'User not found'}, 404