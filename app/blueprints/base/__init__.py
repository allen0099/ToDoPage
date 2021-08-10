from flask import Blueprint

base: Blueprint = Blueprint("base", __name__)
from .root import root
from .todo import new_todo
from .todo import edit_todo
from .todo import delete_todo
