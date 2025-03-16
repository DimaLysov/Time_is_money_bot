from sqlalchemy import select, and_

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Notice

async def get_notice(chat_id: int, name_notice: str | None, id_notice=None):
    user = await get_user(chat_id)
    async with async_session() as session:
        if id_notice is None:
            notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user.id,
                Notice.name_notice == name_notice
            )))
        else:
            notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user.id,
                Notice.id == id_notice
            )))
        return notice