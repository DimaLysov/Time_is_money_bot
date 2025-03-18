from datetime import datetime

import pytz
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.Notice_db.add_notice_db import add_notice
from db.Users.get_user_db import get_user
from filters.day_before_fillter import DayBeforeFilter
from filters.time_notice_filter import TimeNoticeFilter
from keyboards.inline_kb.menu_kb import main_start_inline_kb
from states.all_states import FormAddNotice, FormAddPayment, FormEditPayment
from utils.all_time_zone import rus_time_zone

add_notice_router = Router()


@add_notice_router.callback_query(F.data == 'new_notice_call')
async def call_new_notice(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await request_day_before(call.message, state)


async def request_day_before(m: Message, state: FSMContext):
    await m.answer(text='Введите за сколько дней будет приходить уведомление\n\n'
                        '<i>Например - если нужно присылать за два дня, то вводите 2</i>', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FormAddNotice.day_notice)


@add_notice_router.message(FormAddNotice.day_notice, DayBeforeFilter())
async def request_time_notice(m: Message, state: FSMContext):
    await state.update_data(day_notice=m.text)
    user = await get_user(m.from_user.id)
    await m.answer(text=f'Введите время уведомления в формате час:минуты\n\n'
                        f'<i>Например - {datetime.now(pytz.timezone(rus_time_zone[user.time_zone])).time().strftime("%H:%M")}</i>')
    data = await state.get_data()
    if data.get('add_payment'):
        await state.set_state(FormAddPayment.time_notice)
    elif data.get('edit_payment'):
        await state.set_state(FormEditPayment.time_notice)
    else:
        await state.set_state(FormAddNotice.time_notice)


@add_notice_router.message(FormAddNotice.time_notice, TimeNoticeFilter())
async def accept_time_notice(m: Message, state: FSMContext):
    time_notice = m.text
    info = await state.get_data()
    day_notice = info.get('day_notice')
    creator = 'user'
    answer = await add_notice(m.from_user.id, int(day_notice), time_notice, creator)
    if answer:
        await m.answer(text='Вы успешно добавили уведомление')
    else:
        await m.answer(text='Такое уведомление уже есть')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


# Ниже ловим ошибки при вводе

@add_notice_router.message(FormAddNotice.day_notice)
async def error_day_before(m: Message, state: FSMContext):
    await m.answer(text='День введен не корректно')
    await state.set_state(FormAddNotice.day_notice)


@add_notice_router.message(FormAddNotice.time_notice)
async def error_time_notice(m: Message, state: FSMContext):
    await m.answer(text='Время введено не корректно')
    await state.set_state(FormAddNotice.time_notice)
