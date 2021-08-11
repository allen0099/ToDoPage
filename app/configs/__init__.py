import os


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    USE_SESSION_FOR_NEXT = True

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class Development(Config):
    SQLALCHEMY_DATABASE_URI: str = f'mysql://{os.getenv("SQL_ADMIN")}:{os.getenv("SQL_PASSWORD")}' \
                                   f'@{os.getenv("SQL_LOC")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_SCHEMA")}'


class Testing(Config):
    SECRET_KEY: str = "TEST_KEY"
    TESTING = True
    SQL_ADMIN = "test"
    SQL_PASSWORD = "password"
    SQL_LOCATION = "192.168.0.10"

    SQLALCHEMY_DATABASE_URI: str = f'mysql://{SQL_ADMIN}:{SQL_PASSWORD}@{SQL_LOCATION}:3306/unit_test'


config: dict = {
    "development": Development,
    "testing": Testing,
}
