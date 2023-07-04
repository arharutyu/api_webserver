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

def check_item_in_prop(item_id, prop_id):
    stmt = db.select(Item).filter_by(id=item_id, property_id=prop_id)
    item = db.session.scalar(stmt)
    if item:
        return True
    else:
        abort(404, "Item not found in property.")
    
def check_comment_item(item_id, comment_id):
    stmt = db.select(Comment).filter_by(item_id=item_id, id=comment_id)
    com_item = db.session.scalar(stmt)
    if com_item:
        return True
    else:
        abort(404, "Comment not found for this item.")

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['GET'])
@jwt_required()
def all_comments(prop_id, item_id):
    role_required(prop_id)
    check_item_in_prop(item_id, prop_id)
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    return ItemSchema().dump(item), 201

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>/comment', methods=['POST'])
@jwt_required()
def post_comment(prop_id, item_id):
    role_required(prop_id)
    check_item_in_prop(item_id, prop_id)
    comment_info = CommentSchema().load(request.json)
    comment = Comment(
        comment = comment_info['comment'],
        date_created = date.today(),
        item_id = item_id,
        user_id = get_jwt_identity()
    )

    db.session.add(comment)
    db.session.commit()
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalars(stmt)

    return ItemSchema(many=True).dump(item), 201

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>/comment/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(prop_id, item_id, comment_id):
    access_required()
    check_item_in_prop(item_id, prop_id)
    check_comment_item(item_id, comment_id)
    stmt = db.select(Comment).filter_by(id=comment_id)
    comment = db.session.scalar(stmt)
    db.session.delete(comment)
    db.session.commit()
    return {"Success": "Comment deleted successfully"}, 200