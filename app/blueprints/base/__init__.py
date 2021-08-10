from flask import Blueprint

base: Blueprint = Blueprint("base", __name__)
from .root import root
