import datetime

from app import scheduler
from app.models import Todo, User
from .to_telegram import to_telegram


def add_notify(todo: Todo) -> bool:
    owner: User = User.query.filter_by(id=todo.owner_id).first()

    todo_time: datetime = datetime.datetime.combine(todo.date, todo.time)
    now_time: datetime = datetime.datetime.now()
    reminds_before: datetime.timedelta = datetime.timedelta(minutes=15)

    if owner.telegram_cid and todo_time > now_time + reminds_before:
        scheduler.add_job(f"{owner.id}_{todo.id}", func=to_telegram, args=(owner, todo,),
                          next_run_time=todo_time - reminds_before)
        return True
    return False
