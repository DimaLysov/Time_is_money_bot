from datetime import datetime

from sqlalchemy import select, and_

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice


async def edit_notice_data(chat_id: int, name_notice: str, edit_data: str, new_value):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.name_notice == name_notice
        )))
        if notice:
            if edit_data == 'За сколько дней':
                notice.day_before = new_value
            elif edit_data == 'Время':
                notice.time_send = datetime.strptime(new_value, "%H:%M").time()
            await session.commit()
            notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user_id,
                Notice.name_notice == name_notice
            )))
            notice.name_notice = f'за {notice.day_before} д в {notice.time_send.strftime("%H:%M")}'
            await session.commit()
            return True
        return False