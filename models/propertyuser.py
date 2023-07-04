from init import db

class PropertyUser(db.Model):
    # define the table name for the db
    __tablename__= "propertiesusers"

    role = db.Column(db.String())

    # two foreign & primary keys
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    user = db.relationship('User', back_populates='propertiesusers')

    property_id = db.Column(db.Integer(), db.ForeignKey('properties.id', ondelete='CASCADE'), primary_key=True)
    property = db.relationship('Property', back_populates='propertiesusers')