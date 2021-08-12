from .base_config import Config


class Testing(Config):
    SECRET_KEY: str = "TEST_KEY"
    TESTING = True
    SQL_ADMIN = "test"
    SQL_PASSWORD = "password"
    SQL_LOCATION = "192.168.0.10"

    SQLALCHEMY_DATABASE_URI: str = f'mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOCATION}:3306/unit_test'
