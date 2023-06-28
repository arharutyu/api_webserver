from init import ma 

class PropertySchema(ma.Schema):
    class Meta:
        fields = ('address', 'id')

property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)