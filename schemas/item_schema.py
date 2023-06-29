from init import ma 
from marshmallow import fields

class ItemSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user', 'item']))

    class Meta:
        fields = ('item_name', 'item_desc', 'id', 'user', 'comments')

item_schema = ItemSchema()
itemss_schema = ItemSchema(many=True)