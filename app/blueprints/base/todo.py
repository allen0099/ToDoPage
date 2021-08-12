from flask import abort, redirect, request, url_for
from flask_login import current_user, login_required

from ..base import base
from ...models import Todo


@base.route("/todo", methods=["POST"])
@login_required
def new_todo():
    data: dict = request.form
    # todo: translate time input into UTC time
    content: str = data.get("content")
    time: str = data.get("time")
    date: str = data.get("date")

    todo = Todo(current_user.id, content, time, date)
    todo.new()

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

    todo.edit(content, time, date)

    return redirect(url_for("base.root"))


@base.route("/todo/delete/<int:todo_id>", methods=["POST"])
@login_required
def delete_todo(todo_id: int):
    todo: Todo = Todo.query.filter_by(id=todo_id).first_or_404()

    if todo.owner_id != current_user.id:
        return abort(403)

    todo.delete()

    return redirect(url_for("base.root"))
