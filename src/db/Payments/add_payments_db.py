from sqlalchemy import select, and_

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Payment

async def add_payment(chat_id: int, notice_id: int, name: str, cost: int, date: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user_id,
            Payment.name_payment == name,
            Payment.cost_payment == cost,
            Payment.payment_day == date
        )))
        if not payment:
            session.add(Payment(user_id=user_id,
                                notice_id=notice_id,
                                name_payment=name,
                                cost_payment=cost,
                                payment_day=date))
            await session.commit()
            return True
        return False
