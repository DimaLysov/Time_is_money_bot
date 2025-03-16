from sqlalchemy import select, and_

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Payment

async def add_payment(chat_id: int, notice_id: int, name: str, cost: int, date: int):
    user = await get_user(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user.id,
            Payment.name_payment == name,
            Payment.cost_payment == cost,
            Payment.payment_day == date
        )))
        if not payment:
            session.add(Payment(user_id=user.id,
                                notice_id=notice_id,
                                name_payment=name,
                                cost_payment=cost,
                                payment_day=date))
            await session.commit()
            return True
        return False
