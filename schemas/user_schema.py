from init import ma 

class UserSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password', 'is_admin', 'access', 'id')
        # password = ma.String(validate=Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
