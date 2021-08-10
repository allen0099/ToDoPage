import bcrypt
from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    __tablename__: str = "user"

    id: str = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    username: str = db.Column(db.String(30), nullable=False, unique=True)
    password: str = db.Column(db.String(256), nullable=False)
    name: str = db.Column(db.String(30), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(bytes(password, 'utf-8'), salt).decode('utf-8')

    def is_correct_password(self, password: str) -> bool:
        if bcrypt.checkpw(bytes(password, 'utf-8'), bytes(self.password, 'utf-8')):
            return True
        return False

    def __repr__(self) -> str:
        return f"<User {self.id}>"
