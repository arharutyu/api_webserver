from flask import Blueprint, request, abort
from datetime import timedelta
from models.user import User
from models.propertyuser import PropertyUser
from schemas.user_schema import UserSchema
from init import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
# This blueprint handles authentication

# Fx to use for routes that require admin privilege 
# This is needed to protect lower level access privileges from performing crucial business tasks
# For example: deleting users or properties
def admin_required():
  # Get logged in user id
  user_id = get_jwt_identity()
  # Query database User table and filter to logged in user
  stmt = db.select(User).filter_by(id=user_id)
  # Create object to read
  user = db.session.scalar(stmt)
  # Abort to interrupt execution unless user exists, and user is_admin marked True
  if not (user and user.is_admin):
    abort(401, description="You must be an admin.")

# Fx to use for routes that require access privilege
# This is used for property managers to have access to all users and properties within the database
def access_required():
  # Get logged in user id
  user_id = get_jwt_identity()
  # Query database User table and filter to logged in user
  stmt = db.select(User).filter_by(id=user_id)
  # Create object to read
  user = db.session.scalar(stmt)
  # Abort to interrupt execution unless user exists, and user access OR is_admin marked True
  if not (user and (user.is_admin or user.access)):
    abort(401, description="You don't have access to this resource.")

# Fx to use for routes that require user to have role in property
# This is needed to protect private information of irrelevant properties and other users from tenants
def role_required(prop_id):
  # Get logged in user id
  user_id = get_jwt_identity()
  # Query database User table and filter to logged in user
  stmt = db.select(User).filter_by(id=user_id)
  # Create object to read
  user = db.session.scalar(stmt)
  # Query database PropertyUser table and filter to logged in user and passed in property id
  stmt = db.Select(PropertyUser).filter_by(property_id=prop_id, user_id=user_id)
  # Create object to read
  role = db.session.scalars(stmt).all()
  # Abort to interrupt execution unless user exists, and user access OR is_admin marked True, OR length of role object is greater than zero (meaning user has been assigned to role in relevant property)
  if not (user and (user.is_admin or user.access or len(role)>0)):
    abort(401, description="You don't have access to this resource.")

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Query database User table and filter to email provided by POST request
        stmt = db.select(User).filter_by(email=request.json['email'])
        # Create object to read
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # If user exists, and password entered matches stored password after hashing, create access token
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            # Return user information, less password, and access token
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            # Return error if user and hashed password do not match
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        # Handle error if user and password are not provided.
        return {'error': 'Email and password are required'}, 400





