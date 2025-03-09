from aiogram.filters import BaseFilter
from aiogram.types import Message


class DayPaymentFilter(BaseFilter):
    async def __call__(self, m: Message):
        if not m.text is None:
            if m.text.isdigit():
                return 0 < int(m.text) < 32
        return False