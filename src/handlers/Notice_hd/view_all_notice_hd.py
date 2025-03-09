from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from db.Notice_db.get_all_notices_person import get_notices_user
from keyboards.inline_kb.menu_kb import main_start_inline_kb

view_notice_router = Router()


@view_notice_router.callback_query(F.data == 'view_notice_call')
async def call_view_notice(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_notices_user(call.from_user.id)
    if answer is not None and answer:
        text = '<b>Все ваши уведомления</b>\n\n'
        for notice in answer:
            text += f'— {notice["name_notice"]}'
            if notice["creator"] == 'bot':
                text += f' (<i>стандартное</i>)'
            text += '\n\n'
        await call.message.answer(text=text)
    else:
        await call.message.answer(text='У вас нет ни одного уведомления')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
