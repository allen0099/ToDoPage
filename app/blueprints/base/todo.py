from flask import abort, redirect, request, url_for
from flask_login import current_user, login_required

from ..base import base
from ... import db
from ...models import Todo


@base.route("/todo", methods=["POST"])
@login_required
def new_todo():
    data: dict = request.form
    # todo: translate time input into UTC time
    content: str = data.get("content")
    time: str = data.get("time")
    date: str = data.get("date")

    t = Todo()
    t.owner_id = current_user.id
    t.content = content
    t.time = time
    t.date = date

    db.session.add(t)
    db.session.commit()

    return redirect(url_for("base.root"))


@base.route("/todo/<int:todo_id>", methods=["POST"])
@login_required
def edit_todo(todo_id: int):
    todo: Todo = Todo.query.filter_by(id=todo_id).first_or_404()

    if todo.owner_id != current_user.id:
        return abort(403)

    data: dict = request.form
    # todo: translate time input into UTC time
    content: str = data.get("content")
    time: str = data.get("time")
    date: str = data.get("date")

    todo.content = content
    todo.time = time
    todo.date = date

    db.session.commit()

    return redirect(url_for("base.root"))


@base.route("/todo/delete/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id: int):
    todo: Todo = Todo.query.filter_by(id=todo_id).first_or_404()

    if todo.owner_id != current_user.id:
        return abort(403)

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("base.root"))
