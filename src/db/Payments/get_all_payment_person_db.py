from sqlalchemy import select, and_, asc

from src.db.Users.get_user_id_db import get_user_id
from src.db.models import async_session
from src.db.models import Payment, Notice

async def get_payments_user(chat_id: int):
    user_id = await get_user_id(chat_id)
    async with async_session() as session:
        payments = await session.execute(select(Payment, Notice)
        .join(Notice, Payment.notice_id == Notice.id)
        .filter(and_(
            Payment.user_id == user_id
        ))
        .order_by(asc(Payment.payment_date)))
        if payments:
            list_payments = [
                {
                    'name_payment': payment.name_payment,
                    'cost_payment': payment.cost_payment,
                    'payment_date': payment.payment_date,
                    'name_notice': notice.name_notice
                }
                for payment, notice in payments
            ]
            return list_payments
        return None