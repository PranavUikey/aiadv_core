import json
import os
from datetime import datetime, timedelta

LOG_FILE = "sent_log.json"
COOLDOWN_DAYS = 7


def _load():
    if not os.path.exists(LOG_FILE):
        return {}
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def was_sent(email: str, course: str) -> bool:
    data = _load()
    key = f"{email}|{course}"

    if key not in data:
        return False

    last_sent = datetime.fromisoformat(data[key])
    return datetime.utcnow() - last_sent < timedelta(days=COOLDOWN_DAYS)


def mark_sent(email: str, course: str):
    data = _load()
    key = f"{email}|{course}"
    data[key] = datetime.utcnow().isoformat()
    _save(data)
