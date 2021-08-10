from flask import redirect, render_template, url_for
from flask_login import current_user

from ..base import base


@base.route("/")
def root():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    else:
        return render_template("root.html")
