from sqlalchemy import select, and_

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice

async def get_notice_id(chat_id: int, name_notice: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.name_notice == name_notice
        )))
        if notice:
            return notice.id
        return None