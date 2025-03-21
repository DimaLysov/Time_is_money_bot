from sqlalchemy import select, and_, update

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Payment


async def change_notice_payments(chat_id: int, old_notice_id: int, new_notice_id: int):
    user = await get_user(chat_id)
    async with async_session() as session:
        while True:
            payment = await session.scalar(select(Payment).filter(and_(
                Payment.user_id == user.id,
                Payment.notice_id == old_notice_id
            )))
            if payment:
                payment.notice_id = new_notice_id
                await session.commit()
            else:
                break
        return True
