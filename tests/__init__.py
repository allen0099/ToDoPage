import unittest
from typing import Union

from flask_testing import TestCase

from app import create_app, db
from app.models import User


class Base(TestCase):
    def create_app(self):
        return create_app("testing")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, username: str, name: str, password: str, confirm_password: str = None):
        if not confirm_password:
            confirm_password = password
        return self.client.post("/register",
                                follow_redirects=True,
                                data=dict(
                                    username=username,
                                    name=name,
                                    password=password,
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


class RegisterTest(Base):
    def test_register_pageExist(self):
        # prepare
        template = "register.html"
        # act
        response = self.client.get("/register")
        # valid
        self.assert200(response)
        self.assertTemplateUsed(template)

    def test_register_noDataReturnFlashedMessage(self):
        response = self.client.post('/register',
                                    follow_redirects=True)
        self.assertMessageFlashed("Make sure you had filled up the form!", "danger")

    def test_register_passwordNotMatchReturnFlashedMessage(self):
        username: str = "test"
        name: str = "test_user"
        password: str = "test_password"
        confirm_password: str = "not_match"

        response = self.register(username, name, password, confirm_password)
        self.assertMessageFlashed("Password not match!", "danger")

    def test_register_repeatRegistration(self):
        username: str = "test"
        name: str = "test_user"
        password: str = "test_password"

        response = self.register(username, name, password)
        response = self.register(username, name, password)

        self.assertMessageFlashed("User already exists!", "danger")

    def test_register_success(self):
        username: str = "test"
        name: str = "test_user"
        password: str = "test_password"

        response = self.register(username, name, password)

        self.assertMessageFlashed("Registration successful, please login to continue.", "info")


class LoginTest(Base):
    def test_login_pageExist(self):
        template = "login.html"

        response = self.client.get("/login")

        self.assert200(response)
        self.assertTemplateUsed(template)

    def test_login_noDataLoginReturnFlashMessage(self):
        template = "login.html"

        self.login(None, None)

        self.assertMessageFlashed("Please provide valid username and password!", "danger")
        self.assertTemplateUsed(template)

    def test_login_userNotExistReturnFlashMessage(self):
        username: str = "test"
        password: str = "password"
        not_exist_user: str = "not_exist_user"
        not_exist_password: str = "not_exist_password"
        template = "login.html"

        self.register(username, username, password)
        self.login(not_exist_user, not_exist_password)

        self.assertMessageFlashed("Please provide valid username and password!", "danger")
        self.assertTemplateUsed(template)

    def test_login_userPasswordNotCorrectReturnFlashMessage(self):
        username: str = "test"
        password: str = "password"
        not_correct_password: str = "not_correct_password"
        template = "login.html"

        self.register(username, username, password)
        self.login(username, not_correct_password)

        self.assertMessageFlashed("Credentials not matched!", "danger")
        self.assertTemplateUsed(template)

    def test_login_loginSuccessRedirectToMainPage(self):
        username: str = "test"
        password: str = "password"

        self.register(username, username, password)
        self.login(username, password)
        response = self.client.get("/login")

        self.assertRedirects(response, "/")


class LogoutTest(Base):
    def test_logout(self):
        username: str = "test"
        password: str = "password"

        self.register(username, username, password)
        self.login(username, password)
        response = self.logout()

        self.assertRedirects(response, "/")


class BasePageTest(Base):
    def test_ifNotLoginRedirect(self):
        response = self.client.get("/")

        self.assertRedirects(response, "/login")

    def test_LoginUserRenderPage(self):
        username: str = "test"
        password: str = "password"
        template = "root.html"
        self.register(username, username, password)
        self.login(username, password)

        response = self.client.get("/")

        self.assert200(response)
        self.assertTemplateUsed(template)


class TodoTest(Base):
    def test_new_ifNotLogin(self):
        response = self.client.post("/todo")

        self.assertRedirects(response, "/")

    def test_new_ifLogin(self):
        username: str = "test"
        password: str = "password"
        content: str = "test_data"
        time = "14:28:57"
        date = "2021-02-02"

        self.register(username, username, password)
        self.login(username, password)
        response = self.client.post("/todo",
                                    data=dict(
                                        content=content,
                                        time=time,
                                        date=date,
                                    ))
        user = User.query.filter_by(username=username).first()
        todo_in_db = user.todos[0]

        self.assertEqual(user, todo_in_db.owner)
        self.assertEqual(content, todo_in_db.content)
        self.assertEqual(time, todo_in_db.time.isoformat())
        self.assertEqual(date, todo_in_db.date.isoformat())
        self.assertRedirects(response, "/")

    def test_edit_ifNotLogin(self):
        response = self.client.post("/todo/1")

        self.assertRedirects(response, "/")

    def test_edit_ifLoginAndNotOwned(self):
        had_data_user: str = "test1"
        test_user: str = "test2"
        password: str = "password"
        content: str = "test_data"
        time = "14:28:57"
        date = "2021-02-02"

        self.register(had_data_user, had_data_user, password)
        self.register(test_user, test_user, password)
        self.login(had_data_user, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))
        self.logout()
        new_content = content + "and_new_data"
        new_time = "21:13:41"
        new_date = "2022-11-14"
        self.login(test_user, password)
        response = self.client.post("/todo/1",
                                    data=dict(
                                        content=new_content,
                                        time=new_time,
                                        date=new_date,
                                    ))
        user = User.query.filter_by(username=had_data_user).first()
        had_todo = user.todos[0]

        self.assertEqual(user, had_todo.owner)
        self.assertNotEqual(new_content, had_todo.content)
        self.assertNotEqual(new_time, had_todo.time.isoformat())
        self.assertNotEqual(new_date, had_todo.date.isoformat())
        self.assert403(response)

    def test_edit_ifLoginAndOwned(self):
        username: str = "test"
        password: str = "password"
        content: str = "test_data"
        time = "14:28:57"
        date = "2021-02-02"

        self.register(username, username, password)
        self.login(username, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))

        new_content = content + "and_new_data"
        new_time = "21:13:41"
        new_date = "2022-11-14"
        response = self.client.post("/todo/1",
                                    data=dict(
                                        content=new_content,
                                        time=new_time,
                                        date=new_date,
                                    ))
        user = User.query.filter_by(username=username).first()
        todo = user.todos[0]

        self.assertEqual(user, todo.owner)
        self.assertEqual(new_content, todo.content)
        self.assertEqual(new_time, todo.time.isoformat())
        self.assertEqual(new_date, todo.date.isoformat())
        self.assertRedirects(response, "/")

    def test_delete_ifNotLogin(self):
        response = self.client.post("/todo/delete/1")

        self.assertRedirects(response, "/")

    def test_delete_ifLoginAndNotOwned(self):
        user1: str = "test1"
        user2: str = "test2"
        password: str = "password"
        content: str = "test_data"
        time = "14:28:57"
        date = "2021-02-02"

        self.register(user1, user1, password)
        self.login(user1, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))
        self.logout()
        self.register(user2, user2, password)
        self.login(user2, password)

        response = self.client.post("/todo/delete/1")
        user = User.query.filter_by(username=user1).first()

        self.assertIsNotNone(user.todos)
        self.assert403(response, "/")

    def test_delete_ifLoginAndOwned(self):
        username: str = "test"
        password: str = "password"
        content: str = "test_data"
        time = "14:28:57"
        date = "2021-02-02"

        self.register(username, username, password)
        self.login(username, password)
        self.client.post("/todo",
                         data=dict(
                             content=content,
                             time=time,
                             date=date,
                         ))

        response = self.client.post("/todo/delete/1")
        user = User.query.filter_by(username=username).first()

        self.assertFalse(bool(user.todos))
        self.assertRedirects(response, "/")


if __name__ == '__main__':
    unittest.main()
