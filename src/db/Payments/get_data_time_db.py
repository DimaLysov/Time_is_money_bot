from sqlalchemy import select, and_

from src.db.models import async_session
from src.db.models import Payment, User, Notice


async def get_data_time(now_day, now_time):
    async with async_session() as session:
        result = await session.execute(select(Payment, User, Notice)
        .join(User, Payment.user_id == User.id)
        .join(Notice, Payment.notice_id == Notice.id)
        .filter(and_(
            Payment.payment_date - Notice.day_before == now_day,
            Notice.time_send == now_time
        )))

        # Преобразуем ORM-объекты в списки словарей
        payment_dicts = [
            {
                'id': payment.id,
                'chat_id': user.chat_id,
                'name_payment': payment.name_payment,
                'cost_payment': payment.cost_payment,
                'pyment_date': payment.payment_date,
                'day_before': notice.day_before,
                'time_send': notice.time_send,
            }
            for payment, user, notice in result
        ]
        return payment_dicts
