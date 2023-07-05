from init import db

class Property(db.Model):
    __tablename__ = 'properties'
    # Primary key field, named id
    id = db.Column(db.Integer, primary_key=True)
    # Address field, string type, required
    address = db.Column(db.String, nullable=False, unique=True)
    # Establish relationship between Property and PropertyUsers models
    propertiesusers = db.relationship(
        "PropertyUser",
        back_populates="property",
        cascade="all, delete"
    )
    # Establish relationship between Property and Item models
    items = db.relationship(
        "Item",
        back_populates="property",
        cascade="all, delete"
    )
