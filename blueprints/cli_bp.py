from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.property import Property
from models.propertyuser import PropertyUser
from models.item import Item
from models.comment import Comment
from datetime import date

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

@cli_bp.cli.command("seed")
def seed_db():
    # Create instances of the User model in memory
    users = [
        User(
            first_name='Test',
            last_name='Admin',
            email='admin@test.com',
            password=bcrypt.generate_password_hash('admin12!').decode('utf-8'),
            is_admin=True,
            access = True
        ),
        User(
            first_name='Test',
            last_name='PM',
            email='pm@test.com',
            password=bcrypt.generate_password_hash('user123!').decode('utf-8'),
            is_admin=False,
            access=True
        ),
        User(
            first_name='Flynn',
            last_name='Rider',
            email='flynn@test.com',
            password=bcrypt.generate_password_hash('eugene1!').decode('utf-8'),
            is_admin=False,
            access=False
        )
    ]
    # Delete all existing users
    db.session.query(User).delete()
    # Add instances from above to session
    db.session.add_all(users)
    # Commit changes to database
    db.session.commit()

    # Create instances of the Property model in memory
    properties = [
        Property(
            address="123 Charming Ave"
        ),
        Property(
            address="The Tower in the Woods"
        ),
        Property(
            address="21 Jump St"
        )
    ]
    # Delete all existing properties
    db.session.query(Property).delete()
    # Add instances from above to session
    db.session.add_all(properties)
    # Commit changes to database
    db.session.commit()

    # Create instances of the PropertyUser model in memory
    propertiesusers = [
        PropertyUser(
            role="Property Manager",
            user=users[0],
            property=properties[0]
        ),
        PropertyUser(
            role="Tenant",
            user=users[1],
            property=properties[0]
        )
    ]
    # Delete all existing propertyusers
    db.session.query(PropertyUser).delete()
    # Add instances from above to session
    db.session.add_all(propertiesusers)
    # Commit changes to database
    db.session.commit()

    # Create instances of the Item model in memory
    items = [
        Item(
            item_name = "Teapot",
            item_desc = "Short and stout",
            date_created = date.today(),
            user=users[0],
            property=properties[0]
        ),
        Item(
            item_name = "Dinglehopper",
            item_desc = "Three pronged, silver.",
            date_created = date.today(),
            user=users[0],
            property=properties[1]
        ),
        Item(
            item_name = "Sacred Waterbending Scroll",
            item_desc = "Signs of wear.",
            date_created = date.today(),
            user=users[1],
            property=properties[1]
        )
    ]
    # Delete all existing items
    db.session.query(Item).delete()
    # Add instances from above to session
    db.session.add_all(items)
    # Commit changes to database
    db.session.commit()

    # Create instances of the Item model in memory
    comments = [
        Comment(
            comment = "testing",
            date_created = date.today(),
            items = items[0],
            user = users[0]
        ),
        Comment(
            comment = "one",
            date_created = date.today(),
            items = items[1],
            user = users[0]
        ),
        Comment(
            comment = "two",
            date_created = date.today(),
            items = items[2],
            user = users[0]
        ),
        Comment(
            comment = "checkcheck",
            date_created = date.today(),
            items = items[0],
            user = users[0]
        ),
    ]
    # Delete all existing items
    db.session.query(Comment).delete()
    # Add instances from above to session
    db.session.add_all(comments)
    # Commit changes to database
    db.session.commit()

    print("Models seeded")