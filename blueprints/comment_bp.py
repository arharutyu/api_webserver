from flask import Blueprint, request, abort
from models.property import Property
from schemas.property_schema import PropertySchema
from models.propertyuser import PropertyUser
from schemas.role_schema import RoleSchema
from models.item import Item
from schemas.item_schema import ItemSchema
from models.comment import Comment
from schemas.comment_schema import CommentSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required, access_required
from datetime import date

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['GET'])
@jwt_required()
def all_comments(prop_id, item_id):
    stmt = db.select(Comment).filter_by(item_id=item_id)
    comments = db.session.scalars(stmt)
    return CommentSchema(many=True).dump(comments)

@comment_bp.route('/property/<int:prop_id>/inventory/<int:item_id>', methods=['POST'])
@jwt_required()
def post_comment(prop_id, item_id):
    access_required(prop_id)
    comment_info = CommentSchema().load(request.json)
    comment = Comment(
        comment = comment_info['comment'],
        date_created = date.today(),
        item_id = item_id,
        user_id = get_jwt_identity()
    )

    db.session.add(comment)
    db.session.commit()


    return CommentSchema().dump(comment)