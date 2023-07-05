from init import db

class Item(db.Model):
    __tablename__ = 'items'
    # Primary key field, named id
    id = db.Column(db.Integer, primary_key=True)
    # Item name field, string type max 30 characters
    item_name = db.Column(db.String(30))
    # Item description field, text type
    item_desc = db.Column(db.Text())
    # Date created field, date type
    date_created = db.Column(db.Date())
    # Foreign key field linking to Property model using property_id
    property_id = db.Column(db.Integer(), db.ForeignKey('properties.id', ondelete='CASCADE'))
    # Establish relationship between Property and Item models
    property = db.relationship('Property', back_populates='items')
    # Foreign key field linking to User model using user_id
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # Establish relationship between Comment and User model
    user = db.relationship('User', back_populates='items')
    # Establish relationship between Comment and Item models
    comments = db.relationship('Comment', back_populates='items')
