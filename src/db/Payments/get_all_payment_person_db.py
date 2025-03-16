from sqlalchemy import select, and_, asc

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Payment, Notice

async def get_payments_user(chat_id: int):
    user = await get_user(chat_id)
    async with async_session() as session:
        payments = await session.execute(select(Payment, Notice)
        .join(Notice, Payment.notice_id == Notice.id)
        .filter(and_(
            Payment.user_id == user.id
        ))
        .order_by(asc(Payment.payment_day)))
        if payments:
            list_payments = [
                {
                    'name_payment': payment.name_payment,
                    'cost_payment': payment.cost_payment,
                    'payment_day': payment.payment_day,
                    'name_notice': notice.name_notice
                }
                for payment, notice in payments
            ]
            return list_payments
        return None