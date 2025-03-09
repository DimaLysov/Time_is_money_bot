from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.Payments.get_all_payment_person_db import get_payments_user


class AllAvailablePaymentFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool | dict[str, list[dict]]:
        payment_user = await get_payments_user(m.from_user.id)
        if payment_user:
            return {'list_payments': payment_user}
        return False