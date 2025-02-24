from sqlalchemy import select, and_

from src.db.Notice_db.get_active_notice_db import get_active_notice
from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Payment

async def add_payment(chat_id: int, name: str, cost: int, date: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user_id,
            Payment.name_payment == name,
            Payment.cost_payment == cost,
            Payment.payment_date == date
        )))
        if not payment:
            notice = await get_active_notice(chat_id)
            session.add(Payment(user_id=user_id,
                                notice_id=notice.id,
                                name_payment=name,
                                cost_payment=cost,
                                payment_date=date))
            await session.commit()
            return True
        return False
