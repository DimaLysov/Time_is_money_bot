from sqlalchemy import select, and_

from db.Payments.change_notice_payments_db import change_notice_payments
from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Notice


async def delete_notice(chat_id: int, name_notice: str):
    user = await get_user(chat_id)
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user.id,
            Notice.name_notice == name_notice,
            Notice.creator == 'user'
        )))
        if notice:
            base_notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user.id,
                Notice.creator == 'bot'
            )))
            answer = await change_notice_payments(chat_id, notice.id, base_notice.id)
            if answer:
                await session.delete(notice)
                await session.commit()
                return True
        return False