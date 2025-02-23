from sqlalchemy import select, and_

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Payment, Notice


async def delete_payment(chat_id: int, name_payment: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user_id,
            Payment.name_payment == name_payment
        )))
        if payment:
            await session.delete(payment)
            await session.commit()
            return True
        return False