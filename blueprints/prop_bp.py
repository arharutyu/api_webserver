from flask import Blueprint, request, abort
from models.property import Property
from schemas.property_schema import PropertySchema
from models.propertyuser import PropertyUser
from schemas.role_schema import RoleSchema, AddRoleSchema
from models.item import Item
from schemas.item_schema import ItemSchema, PatchItemSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, access_required, role_required
from datetime import date
from blueprints.comment_bp import check_item_in_prop
from blueprints.user_bp import user_exists


prop_bp = Blueprint('prop', __name__)

def prop_exists(prop_id):
    stmt = db.select(Property).filter_by(id=prop_id)
    prop = db.session.scalar(stmt)
    if prop:
       return True
    else:
       abort(404, "Property not found")

def role_exists(prop_id, user_id):
    stmt = db.select(PropertyUser).filter_by(property_id=prop_id, id=user_id)
    role = db.session.scalars(stmt).all()
    if len(role)<1:
       return False
    else:
        return True

@prop_bp.route('/property', methods=['POST'])
@jwt_required()
def new_prop():
    admin_required()
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
    

@prop_bp.route('/property', methods=['GET'])
@jwt_required()
def all_props():
    access_required()
    stmt = db.select(Property)
    props = db.session.scalars(stmt)
    return PropertySchema(many=True).dump(props)

@prop_bp.route('/property/<int:prop_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_prop(prop_id):
  admin_required()
  prop = prop_exists(prop_id)
  if prop:
      stmt = db.select(Property).filter_by(id=prop_id)
      prop = db.session.scalar(stmt)
      prop_info = PropertySchema().load(request.json)
      prop.address = prop_info.get('address', prop.address)
      db.session.commit()
      return PropertySchema().dump(prop)

@prop_bp.route('/property/<int:prop_id>', methods=['DELETE'])
@jwt_required()
def delete_prop(prop_id):
  admin_required()
  prop = prop_exists()
  if prop:
    stmt = db.select(Property).filter_by(id=prop_id)
    prop = db.session.scalar(stmt)
    db.session.delete(prop)
    db.session.commit()
    return {'success': 'Property successfully deleted'}, 200
  
@prop_bp.route('/property/<int:prop_id>', methods=['GET'])
@jwt_required()
def get_prop(prop_id):
  role_required(prop_id)
  prop = prop_exists(prop_id) 
  if prop:
    stmt = db.select(Property).filter_by(id=prop_id)
    prop = db.session.scalar(stmt)
    return PropertySchema().dump(prop), 201
  
@prop_bp.route('/property/<int:prop_id>/roles', methods=['GET'])
@jwt_required()
def get_roles(prop_id):
   role_required(prop_id)
   prop = prop_exists(prop_id)
   if prop:
    stmt = db.select(Property).filter_by(id=prop_id)
    prop = db.session.scalar(stmt)
    stmt = db.select(PropertyUser).filter_by(property_id=prop_id)
    propuser = db.session.scalars(stmt)
    return [PropertySchema().dump(prop), RoleSchema(many=True).dump(propuser)]
   
@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['POST'])
@jwt_required()
def add_roles(prop_id, user_id):
    access_required()
    prop_exists(prop_id)
    user_exists(user_id)
    role = role_exists(prop_id, user_id)
    if not role:
        stmt = db.select(Property).filter_by(id=prop_id)
        prop = db.session.scalar(stmt)
        new_role = AddRoleSchema().load(request.json)
        propuser = PropertyUser(
            role=new_role['role'],
            user_id = user_id,
            property_id = prop_id)   

                # Add and commit the new prop
        db.session.add(propuser)
        db.session.commit()

        return RoleSchema().dump(propuser), 201
    else:
       abort(400, "User already assigned role at this property.")

@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_roles(prop_id, user_id):
    access_required()
    prop = prop_exists(prop_id)
    user = user_exists(user_id)
    role = role_exists(prop_id, user_id)
    if prop and user and role:
        new_role = AddRoleSchema().load(request.json)
        propuser = PropertyUser(
            role=new_role['role'],
            user_id = user_id,
            property_id = prop_id)   
                # Add and commit the new prop
        db.session.add(propuser)
        db.session.commit()

        return RoleSchema().dump(propuser), 201

@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_role(prop_id, user_id):
    access_required()
    stmt = db.select(Property).filter_by(id=prop_id)
    prop = db.session.scalar(stmt)
    if prop:
        stmt = db.select(PropertyUser).filter_by(property_id=prop_id, user_id=user_id)
        role = db.session.scalar(stmt)
        if role:
            db.session.delete(role)
            db.session.commit()
            return {"Success": "User role deleted from this property"}, 200
        else:
            return {'error': 'User not found to have a role in this property'}, 404
    else:
       return {'error': 'Property not found'}, 404
    
@prop_bp.route('/property/<int:prop_id>/inventory', methods=['GET'])
@jwt_required()
def get_items(prop_id):
    role_required(prop_id)
    prop = prop_exists(prop_id)
    if prop:
        stmt = db.select(Property).filter_by(id=prop_id)
        prop = db.session.scalar(stmt)
        stmt = db.select(Item).filter_by(property_id=prop_id)
        items = db.session.scalars(stmt)
        return ItemSchema(many=True, only=['item_name', 'id']).dump(items), 200
    
@prop_bp.route('/property/<int:prop_id>/inventory', methods=['POST'])
@jwt_required()
def add_item(prop_id):
    access_required()
    prop_exists(prop_id)
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
    return ItemSchema(exclude=['user']).dump(item), 201

@prop_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_item(prop_id, item_id):
    access_required()
    prop_exists(prop_id)
    item = check_item_in_prop(item_id, prop_id)
    if item:
        stmt = db.select(Item).filter_by(id=item_id)
        item = db.session.scalar(stmt)
        item_patch = PatchItemSchema().load(request.json)
        item.item_name = item_patch.get('item_name', item.item_name)
        item.item_desc = item_patch.get('item_desc', item.item_desc)
        item.user_id = get_jwt_identity(),
        item.property_id = prop_id 
        db.session.commit()
        return ItemSchema().dump(item), 201

@prop_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(prop_id, item_id):
  access_required()
  prop_exists(prop_id)
  item = check_item_in_prop(item_id, prop_id)
  if item:
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt) 
    db.session.delete(item)
    db.session.commit()
    return {"Success": "Item has been deleted"}, 200