from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.Notice_db.get_notice_db import get_notice
from src.db.models import Notice


class ExistsNoticeFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool | dict[str, Notice]:
        if not m.text is None:
            notice = await get_notice(m.from_user.id, name_notice=m.text)
            if notice:
                return {'notice': notice}
        return False