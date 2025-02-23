from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.create_bot import bot
from src.db.Payments.get_all_payment_person_db import get_payment_user
from src.keyboards.inline_kb.main_kb import main_start_inline_kb

view_all_payment_router = Router()

@view_all_payment_router.callback_query(F.data == 'view_payment_call')
async def call_view_payment(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_payment_user(call.from_user.id)
    if answer is not None:
        text = ''
        for payment in answer:
            text += (f"{payment['name_payment']} - {payment['cost_payment']}р, {payment['pyment_date']} число\n"
                     f"Уведомление: {payment['name_notice']}\n\n")
        await call.message.answer(text=text)
    else:
        await call.message.answer(text='У вас нет ни одного платежа')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())