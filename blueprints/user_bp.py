from flask import Blueprint, request, abort
from models.user import User
from schemas.user_schema import UserSchema, PatchUserSchema
from init import db, bcrypt
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, access_required

user_bp = Blueprint('user', __name__)
# This blueprint handles users

# Fx to check if user exists
# This is to gracefully handle incorrect user id's provided via endpoints in routes
def user_exists(user_id):
    # Query database User table and filter with user id
    stmt = db.select(User).filter_by(id=user_id)
    # Create object to read
    user = db.session.scalar(stmt)
    # If user exists, return true
    if user:
       return True
    # If query didn't find user with user id, user is not true, abort to interrupt execution
    else:
       abort(404, "User not found")

# Route to register new user
@user_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    # Check user has admin privileges
    admin_required()
    # Validate and sanitize incoming data via Schema
    user_info = UserSchema().load(request.json)
    # Create a new User model instance with the schema data
    user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),
            first_name=user_info['first_name'],
            last_name=user_info['last_name']
        )
    # Get is_admin and access information from schema object
    # This is to ensure that default is set to False if information is not provided in request body
    user.is_admin = user_info.get('is_admin', user.is_admin)
    user.access = user_info.get('access', user.access)
    # Add new user to session
    db.session.add(user)
    # Commit session to database
    db.session.commit()

    # Return the new user, excluding the password
    return UserSchema(exclude=['password']).dump(user), 201

# Route to get all users listed
@user_bp.route('/users')
@jwt_required()
def all_users():
    # Check user permissions for access
    access_required()
    # Query database User table
    stmt = db.select(User)
    # Store in object
    users = db.session.scalars(stmt)
    # Return all users, excluding the password field for each
    return UserSchema(many=True, exclude=['password']).dump(users)

# Route to update current user information
@user_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
  # Check logged in user has admin priviliges
  admin_required()
  # Check user from end point user id exists, error raised via fx if not.
  user = user_exists(user_id)
  if user:
    # Query database Item table and filter with item id
    stmt = db.select(User).filter_by(id=user_id)
    # Store in object
    user = db.session.scalar(stmt)
    # Validate and sanitize incoming data via schema
    user_info = PatchUserSchema().load(request.json)
    # Replace any new information within schema, keep current if not provided
    user.first_name = user_info.get('first_name', user.first_name)
    user.last_name = user_info.get('last_name', user.last_name)
    user.email = user_info.get('email', user.email)
    user.password = bcrypt.generate_password_hash(user_info.get('password', user.password)).decode('utf-8')
    user.is_admin = user_info.get('is_admin', user.is_admin)
    user.access = user_info.get('access', user.access)
    # Commit changes to the database
    db.session.commit()
    # Return updated user information, excluding password
    return UserSchema(exclude=['password']).dump(user), 201
  
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
  # Check logged in user has admin privileges
  admin_required()
  # Check user id passed in exists
  user = user_exists(user_id)
  if user:
    # Query database USer table and filter by user id
    stmt = db.select(User).filter_by(id=user_id)
    # Store in object
    user = db.session.scalar(stmt)
    # Add delete object to session
    db.session.delete(user)
    # Commit changes to database
    db.session.commit()
    return {'Success': 'User deleted'}, 200