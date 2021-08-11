from app.models import User
from tests.test_base import Base


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
