from init import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    propertiesusers = db.relationship(
        "PropertyUser",
        back_populates='user',
        cascade="all, delete"
    )

    items = db.relationship(
        "Item",
        back_populates="user",
        cascade="all, delete"
    )
