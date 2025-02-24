from sqlalchemy import select, and_

from src.db.Notice_db.update_status_notice_db import update_status_notice
from src.db.Payments.change_notice_payments_db import change_notice_payments
from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Notice


async def delete_notice(chat_id: int, name_notice: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        notice = await session.scalar(select(Notice).filter(and_(
            Notice.user_id == user_id,
            Notice.name_notice == name_notice,
            Notice.creator == 'user'
        )))
        if notice:
            if notice.status:
                base_notice = await session.scalar(select(Notice).filter(and_(
                    Notice.user_id == user_id,
                    Notice.creator == 'bot'
                )))
                await update_status_notice(chat_id, base_notice.name_notice)
            active_notice = await session.scalar(select(Notice).filter(and_(
                Notice.user_id == user_id,
                Notice.status.is_(True)
            )))
            answer = await change_notice_payments(chat_id, notice.id, active_notice.id)
            if answer:
                await session.delete(notice)
                await session.commit()
                return True
        return False