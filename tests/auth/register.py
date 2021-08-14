from tests.test_base import Base


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

    def test_register_withTelegramId(self):
        username: str = "test"
        name: str = "test_user"
        password: str = "test_password"
        telegram_id: int = 1234567890

        response = self.register(username, name, password, telegram_id=telegram_id)

        self.assertMessageFlashed("Registration successful, please login to continue.", "info")
