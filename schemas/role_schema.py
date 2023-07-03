from init import ma
from marshmallow import fields, validates_schema
from marshmallow.exceptions import ValidationError
from marshmallow.validate import OneOf

VALID_ROLES = ['Unassigned', 'Property Manager', 'Tenant']

class RoleSchema(ma.Schema):
  user = fields.Nested('UserSchema', only=['first_name', 'last_name', 'id'])
  property = fields.Nested('PropertySchema')
  role = fields.String(load_default=VALID_ROLES[0])

  class Meta:
    fields = ('user', 'role')

class AddRoleSchema(ma.Schema):
  user = fields.Nested('UserSchema', only=['id'])
  property = fields.Nested('PropertySchema')
  role = fields.String()

  @validates_schema()
  def validate_role(self, data, **kwargs):
    role = [x for x in VALID_ROLES if x.upper() == data['role'].upper()]
    if len(role) == 0:
       raise ValidationError(f'Status must be one of: {VALID_ROLES}')
    
    data['role'] = role[0]    

  class Meta:
    fields = ('user_id', 'role')