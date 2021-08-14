from typing import Union

from flask_testing import TestCase

from app import create_app, db, scheduler


class Base(TestCase):
    def create_app(self):
        return create_app("testing")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        scheduler.shutdown()

    def register(self, username: str, name: str, password: str, confirm_password: str = None, telegram_id: int = None):
        if not confirm_password:
            confirm_password = password

        return self.client.post("/register",
                                follow_redirects=True,
                                data=dict(
                                    username=username,
                                    name=name,
                                    password=password,
                                    telegram_cid=telegram_id,
                                    confirm_password=confirm_password
                                ))

    def login(self, username: Union[str, None], password: Union[str, None]):
        return self.client.post("/login",
                                follow_redirects=True,
                                data=dict(
                                    username=username,
                                    password=password,
                                ))

    def logout(self):
        return self.client.post("logout")
