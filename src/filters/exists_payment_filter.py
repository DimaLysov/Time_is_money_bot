from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.Payments.get_payment_db import get_payment
from src.db.models import Payment


class ExistsPaymentFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool | dict[str, Payment]:
        if not m.text is None:
            payment = await get_payment(m.from_user.id, m.text)
            if payment:
                return {'payment': payment}
        return False