from flask import Blueprint, request, abort
from models.property import Property
from schemas.property_schema import PropertySchema
from models.propertyuser import PropertyUser
from schemas.role_schema import RoleSchema, AddRoleSchema
from models.item import Item
from schemas.item_schema import ItemSchema
from models.comment import Comment
from schemas.comment_schema import CommentSchema
from models.user import User
from schemas.user_schema import UserSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, access_required
from datetime import date

prop_bp = Blueprint('prop', __name__)

@prop_bp.route('/property', methods=['POST'])
@jwt_required()
def new_prop():
    admin_required()
    try:
        # Parse, sanitize and validate the incoming JSON data via the schema
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

@prop_bp.route('/property/<int:prop_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_prop(prop_id):
  stmt = db.select(Property).filter_by(id=prop_id)
  prop = db.session.scalar(stmt)
  prop_info = PropertySchema().load(request.json)
  if prop:
    admin_required()
    prop.address = prop_info.get('address', prop.address)
    db.session.commit()
    return PropertySchema().dump(prop)
  else:
    return {'error': 'Property not found'}, 404

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
   
@prop_bp.route('/property/<int:prop_id>/roles', methods=['POST', 'PUT', 'PATCH'])
@jwt_required()
def add_roles(prop_id):
    admin_required()
    new_role = AddRoleSchema().load(request.json)
    propuser = PropertyUser(
            role=new_role['role'],
            user_id=new_role['user_id'],
            property_id = prop_id)   

        # Add and commit the new prop
    db.session.add(propuser)
    db.session.commit()

    return RoleSchema().dump(propuser), 201

@prop_bp.route('/property/<int:prop_id>/roles', methods=['DELETE'])
@jwt_required()
def delete_role(prop_id):
  del_role = AddRoleSchema(only=["user_id"]).load(request.json)
  stmt = db.select(PropertyUser).filter_by(property_id=prop_id, user_id=del_role['user_id'])
  role = db.session.scalar(stmt)
  if role:
    admin_required()
    db.session.delete(role)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'User not found to have a role in this property'}, 404


@prop_bp.route('/property/<int:prop_id>/inventory', methods=['GET'])
@jwt_required()
def get_items(prop_id):
    access_required(prop_id)
    stmt = db.select(Item).filter_by(property_id=prop_id)
    items = db.session.scalars(stmt)
    return ItemSchema(many=True, only=['item_name', 'id']).dump(items)

@prop_bp.route('/property/<int:prop_id>/inventory', methods=['POST'])
@jwt_required()
def add_item(prop_id):
    access_required(prop_id)
    item_info = ItemSchema().load(request.json)
    item = Item(
       item_name = item_info['item_name'],
       item_desc = item_info['item_desc'],
       date_created = date.today(),
       user_id = get_jwt_identity(),
       property_id = prop_id
    )

    db.session.add(item)
    db.session.commit()

    return ItemSchema(exclude=['user']).dump(item)

@prop_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(prop_id, item_id):
  stmt = db.select(Item).filter_by(id=item_id)
  item = db.session.scalar(stmt)  

  if item:
    admin_required()
    db.session.delete(item)
    db.session.commit()
    return {}, 200
  else:
    return {'error': 'Item not found in this property inventory'}, 404