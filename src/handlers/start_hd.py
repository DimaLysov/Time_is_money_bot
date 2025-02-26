from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.db.Users.user_regisration_db import registration
from src.keyboards.inline_kb.main_kb import main_start_inline_kb, payments_inline_kb, notice_inline_kb

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(m: Message, state):
    await state.clear()
    await registration(m.from_user.id, m.from_user.username)
    await m.answer(text='Добро пожаловать.\n\n'
                        'Данный бот поможет вам своевременно оплачивать ваши подписки и другие платежи\n\n'
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
    await call.message.answer(text='здесь будет инструкция')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
