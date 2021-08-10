from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user

from ..auth import auth
from ...models import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("base.root"))
        return render_template("login.html")
    else:
        data: dict = request.form

        if not data.get("username") \
                or not data.get("password"):
            flash("Please provide valid username and password!", "danger")
            return render_template("login.html")

        user: User = User.query.filter_by(username=data.get("username")).first()

        if not user:
            flash("Please provide valid username and password!", "danger")
            return render_template("login.html")

        if user.is_correct_password(data.get("password")):
            login_user(user)
            return redirect(url_for("base.root"))
        else:
            flash("Credentials not matched!", "danger")
            return render_template("login.html")
