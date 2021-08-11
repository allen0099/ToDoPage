from tests.test_base import Base


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
