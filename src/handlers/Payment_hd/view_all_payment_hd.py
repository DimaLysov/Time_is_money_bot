from aiogram import Router, F
from aiogram.types import CallbackQuery

from create_bot import bot
from db.Payments.get_all_payment_person_db import get_payments_user
from keyboards.inline_kb.menu_kb import main_start_inline_kb

view_all_payment_router = Router()


@view_all_payment_router.callback_query(F.data == 'view_payment_call')
async def call_view_payment(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_payments_user(call.from_user.id)
    if answer and answer is not None:
        text = '<b>Все ваши платежи:</b>\n\n'
        number = 1
        for payment in answer:
            text += (
                f"<b>· {payment['name_payment']}</b>:  {payment['cost_payment']}р, {payment['payment_day']} число (<i>уведомлять {payment['name_notice']}</i>)\n\n")
            number += 1
        await call.message.answer(text=text)
    else:
        await call.message.answer(text='У вас нет ни одного платежа')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
