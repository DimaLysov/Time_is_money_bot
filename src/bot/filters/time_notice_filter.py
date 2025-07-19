import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class TimeNoticeFilter(BaseFilter):
    async def __call__(self, m: Message):
        pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
        match = re.match(pattern, m.text)
        return bool(match)