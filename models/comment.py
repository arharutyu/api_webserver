from init import db

class Comment(db.Model):
    __tablename__ = 'comments'
    # Primary key field, named id
    id = db.Column(db.Integer, primary_key=True)
    # Comment field, text type
    comment = db.Column(db.Text())
    # Date created field, date type
    date_created = db.Column(db.Date())
    # Foreign key linking to Items model using item_id
    item_id = db.Column(db.Integer(), db.ForeignKey('items.id', ondelete='CASCADE'))
    # Establish relationship between Comment and Item models
    items = db.relationship('Item', back_populates='comments')
    # Foreign key linking to Users model using user_id
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    # Establish relationship between User and Comment models
    user = db.relationship('User', back_populates='comments')
