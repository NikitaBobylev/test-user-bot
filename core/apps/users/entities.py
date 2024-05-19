import datetime
from dataclasses import dataclass


@dataclass
class User:
    telegram_id: str
    stage: str
    to_send_message: datetime.datetime