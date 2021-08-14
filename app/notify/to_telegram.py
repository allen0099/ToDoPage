import html

import requests

from app.models import Todo, User
from main import app


def to_telegram(owner: User, todo: Todo) -> bool:
    tg_api_url = f"https://api.telegram.org/bot{app.config.get('TELEGRAM_TOKEN')}/sendMessage"

    target = owner.telegram_cid

    if not target:
        return False

    message = html.escape(todo.content)
    params = {
        "chat_id": target,
        "text": message
    }

    api_post = requests.post(tg_api_url, data=params)

    if api_post.status_code != 200:
        return False
    return True
