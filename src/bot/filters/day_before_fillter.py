from aiogram.filters import BaseFilter
from aiogram.types import Message


class DayBeforeFilter(BaseFilter):
    async def __call__(self, m: Message):
        if not m.text is None:
            if m.text.isdigit():
                return int(m.text) < 28
        return False