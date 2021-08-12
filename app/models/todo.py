from app import db


class Todo(db.Model):
    __tablename__: str = "todo"

    id: int = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    owner_id: int = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def new(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, new_content, new_time, new_date):
        self.content = new_content
        self.time = new_time
        self.date = new_date

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, owner_id, content, time, date):
        self.owner_id = owner_id
        self.content = content
        self.time = time
        self.date = date

    def __repr__(self) -> str:
        return f"<Todo {self.id}>"
