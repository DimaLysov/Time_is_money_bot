from datetime import datetime

from sqlalchemy import select, and_

from src.db.Notice_db.update_status_notice_db import update_status_notice
from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice


async def add_notice(chat_id: int, day: int, time: str, period: str, creator: str):
    user_id = await get_user_id(chat_id)
    name_new_notice = f'за {day} д в {time}'
    time = datetime.strptime(time, "%H:%M").time()
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.day_before == day,
            Notice.time_send == time
        )))
        if not notice:
            session.add(Notice(user_id=user_id,
                               name_notice=name_new_notice,
                               day_before=day,
                               time_send=time,
                               period=None if period == '-' else datetime.strptime(period, "%H:%M").time(),
                               creator=creator))
            await session.commit()
            new_notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user_id,
                Notice.name_notice == name_new_notice
            )))
            if new_notice.creator == 'bot':
                await update_status_notice(chat_id, new_notice.name_notice)
            return True
        return False
