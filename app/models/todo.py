from app import db


class Todo(db.Model):
    __tablename__: str = "todo"

    id: int = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    owner_id: int = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    content: str = db.Column(db.Text, nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    @staticmethod
    def new(todo: "Todo"):
        db.session.add(todo)
        db.session.commit()

        from app.notify import add_notify
        add_notify(todo)

    @staticmethod
    def edit(todo: "Todo", new_content, new_time, new_date):
        todo.content = new_content
        todo.time = new_time
        todo.date = new_date

        db.session.commit()

        from app.notify import add_notify, remove_notify
        remove_notify(f"{todo.owner_id}_{todo.id}")
        add_notify(todo)

    @staticmethod
    def delete(todo: "Todo"):
        from app.notify import remove_notify
        remove_notify(f"{todo.owner_id}_{todo.id}")

        db.session.delete(todo)
        db.session.commit()

    def __init__(self, owner_id, content, time, date):
        self.owner_id = owner_id
        self.content = content
        self.time = time
        self.date = date

    def __repr__(self) -> str:
        return f"<Todo {self.id}>"
