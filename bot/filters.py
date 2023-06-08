from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from database import session
from models import UnregisteredUser, RegisteredUser
import datetime


class UserAccessFilter(BaseFilter):
    def __init__(self) -> None:
        ...

    async def __call__(self, message: Message) -> Any:
        user = (
            session.query(RegisteredUser)
            .filter(RegisteredUser.telegram_id == message.from_user.id)
            .first()
        )
        if user is not None:
            user.last_sent_message = datetime.datetime.utcnow()
            session.commit()
            return True
        user = (
            session.query(UnregisteredUser)
            .filter(UnregisteredUser.telegram_id == message.from_user.id)
            .first()
        )
        if user is not None:
            user.last_sent_message = datetime.datetime.utcnow()
        else:
            to_insert = UnregisteredUser(
                telegram_id=message.from_user.id, name=message.from_user.full_name
            )
            session.add(to_insert)
        session.commit()
        return False
