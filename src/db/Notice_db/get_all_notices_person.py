from sqlalchemy import select, and_

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Notice

async def get_notices_user(chat_id: int):
    user = await get_user(chat_id)
    async with async_session() as session:
        notices = await session.scalars(select(Notice).filter(and_(
            Notice.user_id == user.id
        )))
        if notices:
            list_notices = [
                {
                    'name_notice': notice.name_notice,
                    'day_before': notice.day_before,
                    'time_send': notice.time_send,
                    'creator': notice.creator
                }
                for notice in notices
            ]
            return list_notices
        return None