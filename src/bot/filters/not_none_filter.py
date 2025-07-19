from aiogram.filters import BaseFilter
from aiogram.types import Message


class NotNoneFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool:
        if not m.text is None:
           return True
        return False