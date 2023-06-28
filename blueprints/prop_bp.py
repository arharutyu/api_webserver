from flask import Blueprint, request, abort
from models.property import Property
from schemas.property_schema import PropertySchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

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