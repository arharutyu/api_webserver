from init import ma 
from marshmallow import fields

class ItemSchema(ma.Schema):
    class Meta:
        user = fields.Nested('UserSchema', only=['first_name', 'last_name'])

        fields = ('item_name', 'user')

item_schema = ItemSchema()
itemss_schema = ItemSchema(many=True)