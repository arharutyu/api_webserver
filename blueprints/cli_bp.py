from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.property import Property
from models.propertyuser import PropertyUser

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created successfully")

@cli_bp.cli.command("drop")
def create_db():
    db.drop_all()
    print("Tables dropped successfully")

@cli_bp.cli.command("seedu")
def seed_db():
    users = [
        User(
            first_name='Test',
            last_name='Admin',
            email='admin@test.com',
            password=bcrypt.generate_password_hash('admin').decode('utf-8'),
            is_admin=True
        ),
        User(
            first_name='Test',
            last_name='User',
            email='user@test.com',
            password=bcrypt.generate_password_hash('user').decode('utf-8'),
            is_admin=False
        )
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()

@cli_bp.cli.command("seedp")
def seed_prop():
    # Create an instance of the Property model in memory
    properties = [
        Property(
            address="123 Charming Ave"
        ),

        Property(
            address="21 Jump St"
        )
    ]

    db.session.query(Property).delete()
    db.session.add_all(properties)
    db.session.commit()

@cli_bp.cli.command("seedpu")
def seed_propu():
    propertiesusers = [
        PropertyUser(
            role="Property Manager",
            user=users[0],
            property=properties[0]
        ),
        PropertyUser(
            role="Property Manager",
            user=users[0],
            property=properties[0]
        )
    ]

    db.session.query(PropertyUser).delete()
    db.session.add_all(propertiesusers)
    db.session.commit()

    print("Models seeded")

