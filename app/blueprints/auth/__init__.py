from flask import Blueprint

auth: Blueprint = Blueprint("auth", __name__)
from .login import login
from .logout import logout
from .register import register