from flask import flash, redirect, render_template, request, url_for

from ..auth import auth
from ... import db
from ...models import User


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        data: dict = request.form

        if not data.get("username") \
                or not data.get("name") \
                or not data.get("password") \
                or not data.get("confirm_password"):
            flash("Make sure you had filled up the form!", "danger")
            return render_template("register.html")

        if data.get("password") != data.get("confirm_password"):
            flash("Password not match!", "danger")
            return render_template("register.html")

        exist_check: User = User.query.filter_by(username=data.get("username")).first()

        if exist_check:
            flash("User already exists!", "danger")
            return render_template("register.html")

        u: User = User(data.get("username"), data.get("password"))
        u.name = data.get("name")

        if data.get("telegram_cid") and data.get("telegram_cid") != "0":
            u.telegram_cid = data.get("telegram_cid")

        db.session.add(u)
        db.session.commit()

        flash("Registration successful, please login to continue.", "info")
        return redirect(url_for("auth.login"))
