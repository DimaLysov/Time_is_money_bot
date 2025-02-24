from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.create_bot import bot
from src.db.Notice_db.get_all_notice_person import get_notice_user
from src.keyboards.inline_kb.main_kb import main_start_inline_kb

view_notice_router = Router()


@view_notice_router.callback_query(F.data == 'view_notice_call')
async def call_view_notice(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_notice_user(call.from_user.id)
    if answer is not None and answer:
        text = ''
        for notice in answer:
            text += f'{notice["name_notice"]}'
            if notice["status"]:
                text += f' (активное)'
            text += '\n\n'
        await call.message.answer(text=text)
    else:
        await call.message.answer(text='У вас нет ни одного уведомления')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
