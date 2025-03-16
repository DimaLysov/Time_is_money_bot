from sqlalchemy import select, and_

from db.models import async_session
from db.models import User

async def get_user(chat_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(and_(
            User.chat_id == chat_id
        )))
        if not user:
            return None
        return user