from init import db

class User(db.Model):
    __tablename__ = 'users'
    # Primary key field, named id
    id = db.Column(db.Integer, primary_key=True)
    # First name field, string type, max 30 characters, required
    first_name = db.Column(db.String(30), nullable=False)
    # Last name field, string type, max 30 characters, required
    last_name = db.Column(db.String(50), nullable=False)
    # Email field, string type, required, must be unique
    email = db.Column(db.String, nullable=False, unique=True)
    # Password field, string type, required
    password = db.Column(db.String, nullable=False)
    # is_admin field, defaults to False unless provided
    is_admin = db.Column(db.Boolean, default=False)
    # access field, defaults to False unless provided
    access = db.Column(db.Boolean, default=False)
    # Establish relationship between PropertiesUsers and User models
    propertiesusers = db.relationship(
        "PropertyUser",
        back_populates='user',
        cascade="all, delete"
    )
    # Establish relationship between User and Item models
    items = db.relationship(
        "Item",
        back_populates="user",
        cascade="all, delete"
    )
    # Establish relationship between Comment and User models
    comments = db.relationship('Comment', back_populates='user')