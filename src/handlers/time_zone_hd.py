from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db.Users.edit_time_zone_db import edit_time_zone
from db.Users.get_user_db import get_user
from keyboards.inline_kb.menu_kb import time_zone_kb, main_start_inline_kb, yes_no_kb

time_zone_router = Router()


@time_zone_router.callback_query(F.data == 'time_zone')
async def call_time_zone(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    user = await get_user(call.from_user.id)
    await call.message.answer(text=f'Ваша временная зона: {user.time_zone}\n\n')
    await call.message.answer(text=f'Хотите изменить?', reply_markup=yes_no_kb('time_zone_hd.py'))

@time_zone_router.callback_query(F.data == 'no_call_time_zone_hd.py')
async def call_edit_time_zone(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@time_zone_router.callback_query(F.data == 'yes_call_time_zone_hd.py')
async def call_edit_time_zone(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await request_time_zone(call.message)


async def request_time_zone(m: Message):
    await m.answer(text='Выбери подходящую временную зону', reply_markup=time_zone_kb())


@time_zone_router.callback_query(F.data.startswith('tz_'))
async def accept_time_zone(call: CallbackQuery, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    time_zone = call.data.replace('tz_', '')
    answer = await edit_time_zone(call.from_user.id, time_zone)
    if answer:
        await call.message.answer(text='Вы успешно обновили временную зону')
    else:
        await call.message.answer(text='При изменении произошла ошибка')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
