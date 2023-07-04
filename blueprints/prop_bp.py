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
# This blueprint handles properties, along with it's related entities propertiesusers(i.e. roles), and items (i.e. inventory)

# Fx to check property exists
# This is used to check the property id passed in via end points exist in the database
def prop_exists(prop_id):
    # Query the database Properties table and filter with property id
    stmt = db.select(Property).filter_by(id=prop_id)
    # Store in object
    prop = db.session.scalar(stmt)
    # If object exists, property id is in database, fx returns true
    if prop:
       return True
    else:
       # If property id not in database, prop is not true, abort to interrupt execution
       abort(404, "Property not found")

# Fx to check if user id has role in prop id
# This is used for validation when manipulating data in PropertiesUsers, 
# where altered Boolean result may result in different error messages
def role_exists(prop_id, user_id):
    # Query the database PropertyUser table and filter with property id and user id
    stmt = db.select(PropertyUser).filter_by(property_id=prop_id, user_id=user_id)
    # store in object
    role = db.session.scalars(stmt).all()
    # As role returns with scalars, number of entries can be counted with length
    if len(role)==0:
       # If length of role is zero, no role exists for that user in that property
       return False
    else:
        # If length is not zero, a role exists for that user in that property
        return True

# Route to create new property 
@prop_bp.route('/property', methods=['POST'])
@jwt_required()
def new_prop():
    # Check user admin privileges
    admin_required()
    # Sanitize and validate the incoming JSON data via the schema
    prop_info = PropertySchema().load(request.json)
    # Create a new Property model instance with the schema data
    prop = Property(
            address=prop_info['address']
        )
    # Add the new property to the session
    db.session.add(prop)
    # Commit the changes 
    db.session.commit()
    # Return details of new property
    return PropertySchema().dump(prop), 201

# Route to get all properties
@prop_bp.route('/property', methods=['GET'])
@jwt_required()
def all_props():
    # Check user access privileges
    access_required()
    # Query database Property table
    stmt = db.select(Property)
    # Store in object
    props = db.session.scalars(stmt)
    # Return all property details
    return PropertySchema(many=True).dump(props)

# Route to edit property details
@prop_bp.route('/property/<int:prop_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_prop(prop_id):
  # Check user has admin privileges
  admin_required()
  # Check passed in prop id from endpoint exists in database
  prop = prop_exists(prop_id)
  if prop:
      # Query database Property table and filter with prop id
      stmt = db.select(Property).filter_by(id=prop_id)
      # Store in object
      prop = db.session.scalar(stmt)
      # Validate and sanitize incoming JSON data via schema
      prop_info = PropertySchema().load(request.json)
      # Update fields if provided, get from current instance if not
      prop.address = prop_info.get('address', prop.address)
      # Commit changes to database
      db.session.commit()
      # Return updated property details
      return PropertySchema().dump(prop)

# Route to delete property
@prop_bp.route('/property/<int:prop_id>', methods=['DELETE'])
@jwt_required()
def delete_prop(prop_id):
  # Check user has admin permission
  admin_required()
  # Check passed in prop id from endpoint exists in database
  prop = prop_exists(prop_id)
  if prop:
    # Query database Property table and filter with prop id
    stmt = db.select(Property).filter_by(id=prop_id)
    # Store in object
    prop = db.session.scalar(stmt)
    # Add delete object to session
    db.session.delete(prop)
    # Commit changes to database
    db.session.commit()
    return {'success': 'Property successfully deleted'}, 200

# Route to get single property details  
@prop_bp.route('/property/<int:prop_id>', methods=['GET'])
@jwt_required()
def get_prop(prop_id):
    # Check user has permission for access for passed in prop id from endpoint
    role_required(prop_id)
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id) 
    # Query database Property table and filter with prop id
    stmt = db.select(Property).filter_by(id=prop_id)
    # Store in object
    prop = db.session.scalar(stmt)
    # Return property information
    return PropertySchema().dump(prop), 201

# Route to get list of roles for a property
@prop_bp.route('/property/<int:prop_id>/roles', methods=['GET'])
@jwt_required()
def get_roles(prop_id):
    # Check user has permission for access for passed in prop id from endpoint
    role_required(prop_id)
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Query database Property table and filter with prop id
    stmt = db.select(Property).filter_by(id=prop_id)
    # Store in object
    prop = db.session.scalar(stmt)
    # Query database PropertyUser table and filter with prop id
    stmt = db.select(PropertyUser).filter_by(property_id=prop_id)
    # Store in object
    propuser = db.session.scalars(stmt)
    # Return property details, and all assigned role details for that property.
    return [PropertySchema().dump(prop), RoleSchema(many=True).dump(propuser)]

# Route to assign new role to a property/user
@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['POST'])
@jwt_required()
def add_roles(prop_id, user_id):
    # Check user has access privileges
    access_required()
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Check passed in user id from endpoint exists in database
    user_exists(user_id)
    # Check if passed in prop and user id from endpoint already has role in database
    role = role_exists(prop_id, user_id)
    if role:
        abort(400, "User already assigned role at this property.")
    else:
        # If not already assigned, validate and sanitize incoming JSON data via schema
        new_role = AddRoleSchema().load(request.json)
        # Create new instance of PropertyUser object
        propuser = PropertyUser(
            role=new_role['role'],
            user_id = user_id,
            property_id = prop_id)   

        # Add the new propertyuser to session
        db.session.add(propuser)
        # Commit changes to the database
        db.session.commit()
        # Return new role information
        return RoleSchema().dump(propuser), 201

# Route to update role already assigned to user/property
@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_roles(prop_id, user_id):
    # Check user has access permissions
    access_required()
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Check passed in user id from endpoint exists in database
    user_exists(user_id)
    # Check if passed in prop and user id from endpoint already has role in database
    role = role_exists(prop_id, user_id)
    if role:
        # If role exists, query the database PropertyUser table and filter using passed in user id and prop id from endpoint
        stmt = db.select(PropertyUser).filter_by(user_id=user_id, property_id=prop_id)
        # Store in object
        role = db.session.scalar(stmt)
        # Validate and sanitize incoming JSON data via schema
        new_role = AddRoleSchema().load(request.json)
        # Update fields if provided, otherwise use same value as currently stored
        role.role = new_role.get('role', role.role)
        # Commit the changes
        db.session.commit()
        # Return updated role details
        return RoleSchema().dump(role), 201        
    else:
       abort(404, "User not assigned role at this property.")

# Route to remove user from role in property
@prop_bp.route('/property/<int:prop_id>/roles/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_role(prop_id, user_id):
    # Check if user has access permissions
    access_required()
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Check passed in user id from endpoint exists in database
    user_exists(user_id)
    # Check if passed in prop and user id from endpoint has role in database
    role = role_exists(prop_id, user_id)
    if role:
        # Query database PropertyUser table and filter using passed in values
        stmt = db.select(PropertyUser).filter_by(property_id=prop_id, user_id=user_id)
        # Store in object
        role = db.session.scalar(stmt)
        # Add object deletion to session
        db.session.delete(role)
        # Commit session changes to database
        db.session.commit()
        return {"Success": "User role deleted from this property"}, 200
    else:
        abort(404, "User not assigned role at this property.")

# Route to get all items in a property    
@prop_bp.route('/property/<int:prop_id>/inventory', methods=['GET'])
@jwt_required()
def get_items(prop_id):
    # Check user has permission to view the inventory
    role_required(prop_id)
    # Check passed in prop id from endpoint exists in database
    prop = prop_exists(prop_id)
    if prop:
        # Query database Item table, and filter with passed in prop id
        stmt = db.select(Item).filter_by(property_id=prop_id)
        # Store in object
        items = db.session.scalars(stmt)
        # Return all items related to property
        return ItemSchema(many=True, only=['item_name', 'id']).dump(items), 200

# Route to add item to inventory in a property
@prop_bp.route('/property/<int:prop_id>/inventory', methods=['POST'])
@jwt_required()
def add_item(prop_id):
    # Check user has access permission
    access_required()
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Validate and sanitize incoming JSON data via schema
    item_info = ItemSchema().load(request.json)
    # Create new instance of Item class
    item = Item(
       item_name = item_info['item_name'],
       item_desc = item_info['item_desc'],
       # Information set from auto date fx, user information, or passed in parameters
       date_created = date.today(),
       user_id = get_jwt_identity(),
       property_id = prop_id
    )
    # Add new instance to session
    db.session.add(item)
    # Commit session changes to database
    db.session.commit()
    # Return item details just added
    return ItemSchema(exclude=['user']).dump(item), 201

# Route to edit item data
@prop_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_item(prop_id, item_id):
    # Check user has access permission
    access_required()
    # Check passed in prop id from endpoint exists in database
    prop_exists(prop_id)
    # Check passed in prop and item id from endpoint is related in database
    item = check_item_in_prop(item_id, prop_id)
    if item:
        # Query database Item table, filter by item id
        stmt = db.select(Item).filter_by(id=item_id)
        # Store in object
        item = db.session.scalar(stmt)
        # Validate and sanitize incoming JSON data via schema
        item_patch = PatchItemSchema().load(request.json)
        # Update provided fields, or use current existing fields if not provided
        item.item_name = item_patch.get('item_name', item.item_name)
        item.item_desc = item_patch.get('item_desc', item.item_desc)
        item.user_id = get_jwt_identity(),
        item.property_id = prop_id 
        # Commit changes to the database
        db.session.commit()
        # Return updated item information
        return ItemSchema().dump(item), 201

# Delete item from inventory of a property
@prop_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(prop_id, item_id):
# Check user has access permission
  access_required()
  # Check passed in prop id from endpoint exists in database
  prop_exists(prop_id)
  # Check passed in prop and item id from endpoint is related in database
  item = check_item_in_prop(item_id, prop_id)
  if item:
    # Query database Item table, filter by item id
    stmt = db.select(Item).filter_by(id=item_id)
    # Store in object
    item = db.session.scalar(stmt) 
    # Add delete object to session
    db.session.delete(item)
    # Commit session to database
    db.session.commit()
    return {"Success": "Item has been deleted"}, 200