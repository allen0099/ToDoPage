from flask import redirect, url_for
from flask_login import login_required, logout_user

from ..auth import auth


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("base.root"))
