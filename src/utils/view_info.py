from aiogram.types import Message

from db.Notice_db.get_notice_db import get_notice
from db.models import Payment


async def view_info_payment(m: Message, payment: Payment):
    notice = await get_notice(m.from_user.id, name_notice=None, id_notice=payment.notice_id)
    text = (f'Название: {payment.name_payment}\n'
            f'Стоимость:  {payment.cost_payment}\n'
            f'День оплаты:  {payment.payment_day}\n'
            f'Уведомлять:  {notice.name_notice}')
    return text