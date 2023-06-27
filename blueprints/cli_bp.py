from flask import Blueprint
from init import db, bcrypt
from models.user import User

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

#     # Create an instance of the Card model in memory
#     cards = [
#         Card(
#             title="Start the project",
#             description="Stage 1 - Create an ERD",
#             status="Done",
#             date_created=date.today(),
#             # because relationship is set, you can have user instead of user_id, then users[0].id is shortened
#             user=users[0]
#         ),
#         Card(
#             title="ORM Queries",
#             description="Stage 2 - Implement several queries",
#             status="In Progress",
#             date_created=date.today(),
#             user=users[0]
#         ),
#         Card(
#             title="Marshmallow",
#             description="Stage 3 - Implement jsonify of models",
#             status="In Progress",
#             date_created=date.today(),
#             user=users[1]
#         ),
#     ]

#     # Truncate the Card table
#     db.session.query(Card).delete()

#     # Add the card to the session (transaction)
#     db.session.add_all(cards)

#     # Commit the transaction to the database
#     db.session.commit()

#     comments = [
#         Comment(
#             message="Comment 1",
#             date_created=date.today(),
#             user=users[0],
#             card=cards[1]
#         ),
#         Comment(
#             message="Comment 2",
#             date_created=date.today(),
#             user=users[1],
#             card=cards[1]
#         ),
#         Comment(
#             message="Comment 3",
#             date_created=date.today(),
#             user=users[1],
#             card=cards[0]
#         )
#     ]

#     db.session.query(Comment).delete()
#     db.session.add_all(comments)
#     db.session.commit()

#     print("Models seeded")
