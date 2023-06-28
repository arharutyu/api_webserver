from flask import Blueprint, request, abort
from models.property import Property
from schemas.property_schema import PropertySchema
from models.propertyuser import PropertyUser
from schemas.role_schema import RoleSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, access_required

prop_bp = Blueprint('prop', __name__)

@prop_bp.route('/property', methods=['POST'])
@jwt_required()
def new_prop():
    admin_required()
    try:
        # Parse, sanitize and validate the incoming JSON data
        # via the schema
        prop_info = PropertySchema().load(request.json)
        # Create a new Property model instance with the schema data
        prop = Property(
            address=prop_info['address']
        )

        # Add and commit the new prop
        db.session.add(prop)
        db.session.commit()

        return PropertySchema().dump(prop), 201
    
    except:
        return {'error': 'Something went wrong'}

@prop_bp.route('/property', methods=['GET'])
@jwt_required()
def all_props():
    stmt = db.select(Property)
    props = db.session.scalars(stmt)
    return PropertySchema(many=True).dump(props)

@prop_bp.route('/property/<int:prop_id>', methods=['DELETE'])
@jwt_required()
def delete_prop(prop_id):
  stmt = db.select(Property).filter_by(id=prop_id)
  prop = db.session.scalar(stmt)
  if prop:
    admin_required()
    db.session.delete(prop)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Property not found'}, 404
  
@prop_bp.route('/property/<int:prop_id>', methods=['GET'])
@jwt_required()
def get_prop(prop_id):
  stmt = db.select(Property).filter_by(id=prop_id)
  prop = db.session.scalar(stmt)
  if prop:
    return PropertySchema().dump(prop), 201
  else:
    return {'error': 'Property not found'}, 404
  
@prop_bp.route('/property/<int:prop_id>/roles', methods=['GET'])
@jwt_required()
def get_roles(prop_id):
   access_required(prop_id)
   stmt = db.select(Property).filter_by(id=prop_id)
   prop = db.session.scalar(stmt)
   
   stmt = db.select(PropertyUser).filter_by(property_id=prop_id)
   propuser = db.session.scalars(stmt)
   
   if prop:
      return [PropertySchema().dump(prop), RoleSchema(many=True).dump(propuser)]
   else:
      return {'error': 'Property not found'}, 404
   
# @prop_bp.route('/property/<int:prop_id>/roles', methods=['PUT'])
# @jwt_required()
# def add_roles(prop_id):
#     try:
#         new_role = RoleSchema().load(request.json)
#         propuser = PropertyUser(
#             role=new_role['role']
#         )

#         # Add and commit the new prop
#         db.session.add(propuser)
#         db.session.commit()

#         return RoleSchema(many=True).dump(propuser), 201
    
#     except:
#         return {'error': 'Something went wrong'}