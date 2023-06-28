from flask import Blueprint, request, abort
from datetime import timedelta
from models.user import User
from schemas.user_schema import UserSchema
from init import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

def admin_required():
  user_id = get_jwt_identity()
  stmt = db.select(User).filter_by(id=user_id)
  user = db.session.scalar(stmt)
  if not (user and user.is_admin):
    abort(401, description="You must be an admin.")



@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400




# def admin_or_owner_required(owner_id):
#   user_id = get_jwt_identity()
#   stmt = db.select(User).filter_by(id=user_id)
#   user = db.session.scalar(stmt)
#   if not (user and (user.is_admin or user_id == owner_id)):
#     abort(401, description="You must be an admin or the owner")
