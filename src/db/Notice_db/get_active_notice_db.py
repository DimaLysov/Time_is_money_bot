from datetime import datetime

from sqlalchemy import select, and_

from src.db.Notice_db.update_status_notice_db import update_status_notice
from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice

async def get_active_notice(chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.status.is_(True)
        )))
        if notice:
            return notice.id
        return None