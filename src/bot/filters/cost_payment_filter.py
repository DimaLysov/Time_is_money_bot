from aiogram.filters import BaseFilter
from aiogram.types import Message


class CostPaymentFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool:
        if not m.text is None:
            if m.text.isdigit():
                return 0 < int(m.text) < 2 * 10 ** 9
        return False
