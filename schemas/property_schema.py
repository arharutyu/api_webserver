from init import ma 
from marshmallow import fields

class PropertySchema(ma.Schema):
    address = fields.String(required=True)
    class Meta:
        fields = ('address', 'id')

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True) 