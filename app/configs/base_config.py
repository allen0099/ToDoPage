import os

from dotenv import load_dotenv


class Config:
    load_dotenv(verbose=True)  # load env for unit test
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    USE_SESSION_FOR_NEXT = True

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

    SCHEDULER_TIMEZONE = "Asia/Taipei"
    SCHEDULER_API_ENABLED = False
