from tests.test_base import Base


class LogoutTest(Base):
    def test_logout(self):
        username: str = "test"
        password: str = "password"

        self.register(username, username, password)
        self.login(username, password)
        response = self.logout()

        self.assertRedirects(response, "/")
