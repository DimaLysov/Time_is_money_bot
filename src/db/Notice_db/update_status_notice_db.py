from datetime import datetime

from sqlalchemy import select, and_

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice

async def update_status_notice(chat_id: int, name_new_notice: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        new_notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.name_notice == name_new_notice
        )))
        if not new_notice:
            return False
        now_notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.status.is_(True)
        )))
        if now_notice:
            now_notice.status = False
            await session.commit()
        new_notice.status = True
        await session.commit()
        return True