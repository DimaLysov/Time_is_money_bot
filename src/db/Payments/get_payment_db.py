from sqlalchemy import select, and_

from db.Users.get_user_id_db import get_user_id
from db.models import async_session
from db.models import Payment


async def get_payment(chat_id: int, name_payment: str):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.name_payment == name_payment,
            Payment.user_id == user_id
        )))
        return payment

