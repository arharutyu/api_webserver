from init import ma 
from marshmallow.validate import Length, Regexp
from marshmallow import fields

class UserSchema(ma.Schema):
    password = fields.String(validate=Regexp('^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', error='Password must be at least 8 characters, and must include at least one letter, one number, and one special character.'))
    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password', 'is_admin', 'access', 'id')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)