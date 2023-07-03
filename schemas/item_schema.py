from init import ma 
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And

class ItemSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['item']))
    item_name = fields.String(required=True, validate=And(
     Length(min=3, error='Title must be at least 3 characters long'),
     Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers, and spaces are allowed')
     ))
    item_desc = fields.String(load_default=' ')

    class Meta:
        fields = ('item_name', 'item_desc', 'id', 'user', 'comments')

item_schema = ItemSchema()
itemss_schema = ItemSchema(many=True)

class PatchItemSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['first_name', 'last_name'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user', 'item']))
    item_name = fields.String(validate=And(
     Length(min=3, error='Title must be at least 3 characters long'),
     Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers, and spaces are allowed')
     ))
    item_desc = fields.String()

    class Meta:
        fields = ('item_name', 'item_desc', 'id', 'user', 'comments')