from init import db

class PropertyUser(db.Model):
    # define the table name for the db
    __tablename__= "propertiesusers"
    # Role field, string type
    role = db.Column(db.String())

    # two foreign & primary keys
    # Primary key 1, also foreign key linking to Users model
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    # Establish relationship between User and PropertyUser models
    user = db.relationship('User', back_populates='propertiesusers')
    # Primary key 2, also foreign key linking to PeropertiesUsers model
    property_id = db.Column(db.Integer(), db.ForeignKey('properties.id', ondelete='CASCADE'), primary_key=True)
    # Establish relationship between Property and PropertyUser models
    property = db.relationship('Property', back_populates='propertiesusers')