from app import db


class Todo(db.Model):
    __tablename__: str = "todo"

    id: int = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    owner_id: int = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    content: str = db.Column(db.String(60), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"<Todo {self.id}>"
