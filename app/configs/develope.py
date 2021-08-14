import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from .base_config import Config


class Development(Config):
    SQLALCHEMY_DATABASE_URI: str = f'mysql://{os.getenv("SQL_ADMIN")}:{os.getenv("SQL_PASSWORD")}' \
                                   f'@{os.getenv("SQL_LOC")}:{os.getenv("SQL_PORT")}/{os.getenv("SQL_SCHEMA")}'
    SCHEDULER_JOBSTORES = {
        "default": SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }
