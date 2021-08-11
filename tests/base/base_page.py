from tests.test_base import Base


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
