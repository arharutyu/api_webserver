from init import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(30))
    item_desc = db.Column(db.Text())
    date_created = db.Column(db.Date())

    property_id = db.Column(db.Integer(), db.ForeignKey('properties.id', ondelete='CASCADE'))
    property = db.relationship('Property', back_populates='items')

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='items')

    comments = db.relationship('Comment', back_populates='items')
