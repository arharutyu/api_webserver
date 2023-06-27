from init import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)

    address = db.Column(db.String, nullable=False, unique=True)