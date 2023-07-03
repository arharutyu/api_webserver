from init import ma 
from marshmallow import fields

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    item = fields.Nested('ItemSchema', only=['item_name'])
    comment = fields.String(required=True)
    date_created = fields.Date()

    class Meta:
        fields = ('comment', 'date_created', 'user', 'item', 'id')


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)