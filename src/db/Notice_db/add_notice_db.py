from datetime import datetime

from sqlalchemy import select, and_

from db.Users.get_user_id_db import get_user_id
from db.models import async_session
from db.models import Notice


async def add_notice(chat_id: int, day: int, time: str, creator: str):
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
                               creator=creator))
            await session.commit()
            return True
        return False
