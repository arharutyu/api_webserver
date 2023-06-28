from init import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    date_created = db.Column(db.Date())

    item_id = db.Column(db.Integer(), db.ForeignKey('items.id', ondelete='CASCADE'))
    item = db.relationship('Item', back_populates='comments')

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='comments')
