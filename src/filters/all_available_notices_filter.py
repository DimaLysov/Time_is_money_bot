from aiogram.filters import BaseFilter
from aiogram.types import Message

from db.Notice_db.get_all_notices_person import get_notices_user


class AllAvailableNoticeFilter(BaseFilter):
    async def __call__(self, m: Message) -> bool | dict[str, list[dict]]:
        notices_user = await get_notices_user(m.from_user.id)
        if len(notices_user) > 1:
            return {'list_notices': notices_user}
        return False