from dataclasses import dataclass


@dataclass
class User:
    telegram_id: str
    stage: str
