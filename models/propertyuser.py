from init import db

class PropertyUser(db.Model):
    # define the table name for the db
    __tablename__= "propertiesusers"

    id = db.Column(db.Integer,primary_key=True)


    role = db.Column(db.String())

    # two foreign keys
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='propertiesusers')

    property_id = db.Column(db.Integer(), db.ForeignKey('properties.id', ondelete='CASCADE'))
    property = db.relationship('Property', back_populates='propertiesusers')