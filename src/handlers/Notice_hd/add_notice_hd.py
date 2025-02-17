from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.db.Notice_db.add_notice_db import add_notice
from src.keyboards.inline_kb.main_kb import main_start_inline_kb
from src.utils.check_fn import check_dey_format, check_time_format

add_notice_router = Router()


class FormAddNotice(StatesGroup):
    day_notice = State()
    time_notice = State()
    period_notice = State()


@add_notice_router.callback_query(F.data == 'new_notice_call')
async def call_new_notice(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Введите за сколько дней будет приходить уведомление\n\n'
                                   '<i>Например - если нужно присылать за два дня, то вводите 2</i>')
    await state.set_state(FormAddNotice.day_notice)


@add_notice_router.message(FormAddNotice.day_notice)
async def accept_day_notice(m: Message, state: FSMContext):
    if not check_dey_format(m.text):
        await m.answer(text='Не корректно указан день, попробуйте еще раз')
        await state.set_state(FormAddNotice.day_notice)
        return
    await state.update_data(day_notice=m.text)
    await m.answer(text=f'Введите время уведомления в формате час:минуты\n\n'
                        f'<i>Например - {datetime.now().time().strftime("%H:%M")}</i>')
    await state.set_state(FormAddNotice.time_notice)


@add_notice_router.message(FormAddNotice.time_notice)
async def accept_time_notice(m: Message, state: FSMContext):
    if not check_time_format(m.text):
        await m.answer(text='Не корректно указано время, попробуйте еще раз')
        await state.set_state(FormAddNotice.time_notice)
        return
    await state.update_data(time_notice=m.text)
    await m.answer(text='Введите периодичность с которой будет напоминать об оплате, пока вы не подтвердите платеж\n\n'
                        '<i>Например - если нужно присылать раз в 45 минут, то вводите 00:45</i>\n\n'
                        'Для пропуска введите "-"')
    await state.set_state(FormAddNotice.period_notice)


@add_notice_router.message(FormAddNotice.period_notice)
async def accept_period(m: Message, state: FSMContext):
    period_notice = m.text
    if not check_time_format(period_notice) and period_notice != '-':
        await m.answer(text='Не корректно указано время, попробуйте еще раз')
        await state.set_state(FormAddNotice.period_notice)
        return
    info = await state.get_data()
    day_notice = info.get('day_notice')
    time_notice = info.get('time_notice')
    answer = await add_notice(m.from_user.id, int(day_notice), time_notice, period_notice)
    if answer:
        await m.answer(text='Вы успешно добавили уведомление')
    else:
        await m.answer(text='Такое уведомление уже есть')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
