from sqlalchemy import select, and_

from db.models import async_session
from db.models import User

async def edit_time_zone(chat_id: int, new_time_zone):
    async with async_session() as session:
        user = await session.scalar(select(User).filter(and_(
            User.chat_id == chat_id
        )))
        if user:
            user.time_zone = new_time_zone
            await session.commit()
            return True
        return False