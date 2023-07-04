from flask import Blueprint, request, abort
from models.item import Item
from schemas.item_schema import ItemSchema
from models.comment import Comment
from schemas.comment_schema import CommentSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import access_required, role_required
from datetime import date

comment_bp = Blueprint('comment', __name__)
# This blueprint handles comments, which is an entity related to items.

# Fx to check if item exists in property
# This is used to check item and property id's entered via endpoints are related
def check_item_in_prop(item_id, prop_id):
    # Query database Item table and filter with item id and property id
    stmt = db.select(Item).filter_by(id=item_id, property_id=prop_id)
    # Create object to read
    item = db.session.scalar(stmt)
    # If item exists in property, then return True to continue route
    if item:
        return True
    # If item id is not found in relevant property, abort to interrupt execution
    else:
        abort(404, "Item not found in property.")

# Fx to check if comment is related to relevant item
# This is used to check item and comment id's entered via endpoints are related
def check_comment_item(item_id, comment_id):
    # Query database Comment table and filter with item id and comment id
    stmt = db.select(Comment).filter_by(item_id=item_id, id=comment_id)
    # Create object to read
    com_item = db.session.scalar(stmt)
    # If comment/item are linked com_item does not return None, return True to continue route
    if com_item:
        return True
    # If comment/item are not linked com_item is None, abort to interrupt execution
    else:
        abort(404, "Comment not found for this item.")

# Route to get single item within inventory of a property
@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['GET'])
@jwt_required()
def all_comments(prop_id, item_id):
    # Check user permissions for current property
    role_required(prop_id)
    # Check item and property are related
    check_item_in_prop(item_id, prop_id)
    # Query database Item table and filter with item id
    stmt = db.select(Item).filter_by(id=item_id)
    # Store in object
    item = db.session.scalar(stmt)
    # Return object details via JSON
    return ItemSchema().dump(item), 201

# Route to add comment to item within inventory of a property
@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>/comment', methods=['POST'])
@jwt_required()
def post_comment(prop_id, item_id):
    # Check user permissions for current property
    role_required(prop_id)
    # Check item and property are related
    check_item_in_prop(item_id, prop_id)
    # Validate and sanitize incoming data via schema
    comment_info = CommentSchema().load(request.json)
    # Create new instance of Comment model in memory
    comment = Comment(
        comment = comment_info['comment'],
        date_created = date.today(),
        item_id = item_id,
        user_id = get_jwt_identity()
    )
    # Add and commit new comment object to database
    db.session.add(comment)
    db.session.commit()
    # Query database Item table and filter with item id. Comments only relate to one item and are not viewed in isolation.
    stmt = db.select(Item).filter_by(id=item_id)
    # Store in object
    item = db.session.scalars(stmt)
    # Return object details via JSON
    # To ensure clarity, the entire Item object (including comments) is returned upon successfully posting a comment
    return ItemSchema(many=True).dump(item), 201

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>/comment/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(prop_id, item_id, comment_id):
    # Check user permissions for access
    access_required()
    # Check item and property are related
    check_item_in_prop(item_id, prop_id)
    # Check item and comment are related
    check_comment_item(item_id, comment_id)
    # Query database Comment table and filter with comment id.
    stmt = db.select(Comment).filter_by(id=comment_id)
    # Store in object
    comment = db.session.scalar(stmt)
    # Add delete comment to session
    db.session.delete(comment)
    # Commit session to finalize
    db.session.commit()
    return {"Success": "Comment deleted successfully"}, 200