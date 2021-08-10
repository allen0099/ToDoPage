import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from app import create_app

load_dotenv(dotenv_path=str(Path(sys.argv[0]).parent / ".env"), verbose=True)

app: Flask = create_app()

if __name__ == '__main__':
    app.run()
