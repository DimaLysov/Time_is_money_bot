from sqlalchemy import select, and_

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Payment, Notice


async def delete_payment(chat_id: int, name_payment: str):
    user = await get_user(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user.id,
            Payment.name_payment == name_payment
        )))
        if payment:
            await session.delete(payment)
            await session.commit()
            return True
        return False