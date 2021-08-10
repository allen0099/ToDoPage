import os


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


class Development(Config):
    SQLALCHEMY_DATABASE_URI: str = f'mysql://{os.getenv("SQL_ADMIN")}:{os.getenv("SQL_PASSWORD")}' \
                                   f'@{os.getenv("SQL_LOC")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_SCHEMA")}'


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


config: dict = {
    "development": Development,
    "testing": Testing,
}
