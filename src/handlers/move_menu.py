from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from src.keyboards.inline_kb.menu_kb import main_start_inline_kb, payments_inline_kb, notice_inline_kb

move_menu_router = Router()


@move_menu_router.callback_query(F.data == 'main_payment')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=payments_inline_kb())


@move_menu_router.callback_query(F.data == 'main_notice')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=notice_inline_kb())


@move_menu_router.callback_query(F.data == 'back_main')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=main_start_inline_kb())


@move_menu_router.callback_query(F.data == 'main_setting')
async def write_payment_kb(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='''<b>Инструкция по использованию:</b>

<b>Для создания платежей необходимо будет указать:</b>

1) Название (может быть любое)
2) Сумма (цену указывать в рублях)
3) Число оплаты (указать только день)
К платежу будет присоединяться ваше активное уведомление

<b>Для создания уведомлений:</b>

1) Указать за сколько дней нужно напоминать об платеже
(<i>введите 0, чтобы уведомление проходило в день оплаты</i>)
2) В какое время это нужно будет сделать

<b>Примечания</b>

— У каждого пользователя всегда есть 1 уведомление: за 1 день в 12:00
— Чтобы выйти из режима создания или редактирования введите команду /menu

<b>Ограничения</b>

— Нельзя создавать платежи с одинаковым названием
— Нельзя создавать одинаковые уведомления
— Стандартное уведомление нельзя поменять или удалить
''')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
