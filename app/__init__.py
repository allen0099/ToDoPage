import inspect

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.configs import config

db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager()
login_manager.login_view = "base.root"


def create_app(name: str = "development") -> Flask:
    app: Flask = Flask(__name__)

    # configs
    app.config.from_object(config[name])

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(uid) -> User:
        # return an User object
        return User.query.filter_by(id=uid).first()

    @app.shell_context_processor
    def make_shell_context() -> dict:
        from app import models

        def rebuild():
            db.drop_all()
            print("Drop successful!")
            db.create_all()
            print("Create successful!")

        return dict(
            db=db,
            rebuild=rebuild,
            **dict(
                inspect.getmembers(models, inspect.isclass)
            )
        )

    @app.cli.command("test")
    def test():
        import unittest
        import sys

        tests = unittest.TestLoader().discover("tests")
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.errors or result.failures:
            sys.exit(1)

    with app.app_context():
        # register blueprints
        from app.blueprints.auth import auth
        app.register_blueprint(auth)

        from app.blueprints.base import base
        app.register_blueprint(base)

        return app
