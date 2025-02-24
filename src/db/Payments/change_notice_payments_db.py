from sqlalchemy import select, and_, update

from src.db.Notice_db.get_active_notice_db import get_active_notice
from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Payment


async def change_notice_payments(chat_id: int, old_notice_id: int, new_notice_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        while True:
            payment = await session.scalar(select(Payment).filter(and_(
                Payment.user_id == user_id,
                Payment.notice_id == old_notice_id
            )))
            if payment:
                payment.notice_id = new_notice_id
                await session.commit()
            else:
                break
        return True
