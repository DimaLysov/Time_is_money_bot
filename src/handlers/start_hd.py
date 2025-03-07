from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.create_bot import bot
from src.db.Users.user_regisration_db import registration
from src.keyboards.inline_kb.menu_kb import main_start_inline_kb, payments_inline_kb, notice_inline_kb

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(m: Message, state):
    await state.clear()
    await registration(m.from_user.id, m.from_user.username)
    await m.answer(text='Добро пожаловать.\n\n'
                        'Данный бот поможет вам своевременно оплачивать ваши ежемесячные подписки и другие платежи\n\n'
                        'Чтобы открыть меню бота нажмите сюда ️ 👉 <b>/menu</b>')


@start_router.callback_query(F.data == 'main_payment')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=payments_inline_kb())


@start_router.callback_query(F.data == 'main_notice')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=notice_inline_kb())


@start_router.callback_query(F.data == 'back_main')
async def write_payment_kb(call: CallbackQuery):
    await call.message.edit_reply_markup(str(call.message.message_id), reply_markup=main_start_inline_kb())


@start_router.callback_query(F.data == 'main_setting')
async def write_payment_kb(call: CallbackQuery):
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
