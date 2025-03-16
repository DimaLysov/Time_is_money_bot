from sqlalchemy import select, and_

from db.Users.get_user_db import get_user
from db.models import async_session
from db.models import Payment


async def edit_date_payment(chat_id: int, now_name: str, edit_data: str, new_value):
    user = await get_user(chat_id)
    async with async_session() as session:
        payment = await session.scalar(select(Payment).filter(and_(
            Payment.user_id == user.id,
            Payment.name_payment == now_name
        )))
        if payment:
            if edit_data == 'Название':
                payment.name_payment = new_value
            elif edit_data == 'Стоимость':
                payment.cost_payment = new_value
            elif edit_data == 'День оплаты':
                payment.payment_day = new_value
            elif edit_data == 'Уведомление':
                payment.notice_id = new_value
            await session.commit()
            return True
        return False

