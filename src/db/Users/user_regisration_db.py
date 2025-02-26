from datetime import datetime

from sqlalchemy import select, and_

from src.db.Notice_db.add_notice_db import add_notice
from src.db.models import async_session
from src.db.models import User


async def registration(chat_id: int, user_name: str):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(and_(
            User.chat_id == chat_id,
            User.user_name == user_name
        )))
        if not user:
            session.add(User(chat_id=chat_id, user_name=user_name))
            await session.commit()
            day = 1
            time = '12:00'
            creator = 'bot'
            await add_notice(chat_id, day, time, creator)
            return True
        return False
