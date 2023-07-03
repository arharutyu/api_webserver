from init import ma 
from marshmallow.validate import Length, Regexp, And
from marshmallow import fields

class UserSchema(ma.Schema):
    password = fields.String(required = True, validate=(
        Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', error='Password must be at least 8 characters, and must include at least one letter, one number, and one special character.')
        ))
    first_name = fields.String(required = True, validate=Length(min=2, max=30))
    last_name = fields.String(required = True, validate=Length(min=2, max=50))
    email = fields.Email(required = True, unique = True)
    is_admin = fields.Bool(default=False)
    access = fields.Bool(default=False)
    
    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password', 'is_admin', 'access', 'id')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class PatchUserSchema(ma.Schema):
    password = fields.String(validate=(
        Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', error='Password must be at least 8 characters, and must include at least one letter, one number, and one special character.')
        ))
    first_name = fields.String(validate=Length(min=2, max=30))
    last_name = fields.String(validate=Length(min=2, max=50))
    email = fields.Email(unique = True)
    is_admin = fields.Bool(default=False)
    access = fields.Bool(default=False)
    
    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password', 'is_admin', 'access', 'id')
 