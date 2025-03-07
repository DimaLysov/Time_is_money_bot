from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.db.Notice_db.add_notice_db import add_notice
from src.db.Notice_db.get_all_notice_person import get_notice_user
from src.db.Notice_db.get_notice_db import get_notice
from src.db.Payments.add_payments_db import add_payment
from src.db.Payments.get_payment_db import get_payment
from src.keyboards.inline_kb.menu_kb import main_start_inline_kb
from src.keyboards.line_kb import kb_choice_notice
from src.utils.check_fn import check_day_payment_format, check_day_notice_format, check_time_format

add_payment_router = Router()


class FormAddPayment(StatesGroup):
    name_payment = State()
    cost_payment = State()
    date_payment = State()
    notice_payment = State()
    day_notice = State()
    time_notice = State()

@add_payment_router.callback_query(F.data == 'new_payment_call')
async def call_add_payment(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Введите название нового платежа')
    await state.set_state(FormAddPayment.name_payment)

@add_payment_router.message(FormAddPayment.name_payment)
async def accept_name_payment(m: Message, state: FSMContext):
    name_payment = m.text
    payment = await get_payment(m.from_user.id, name_payment)
    if not payment:
        await state.update_data(name_payment=m.text)
        await state.set_state(FormAddPayment.cost_payment)
        await m.answer(text='Введи цену вашей подписки (в рублях)')
    else:
        await m.answer(text='Платеж с таким названием уже есть, попробуйте еще раз')
        await state.set_state(FormAddPayment.name_payment)


@add_payment_router.message(FormAddPayment.cost_payment)
async def accept_cost(m: Message, state: FSMContext):
    if not m.text.isdigit():
        await m.answer(text='Некорректно указана цена, попробуйте еще раз')
        await state.set_state(FormAddPayment.cost_payment)
        return
    await state.update_data(cost_payment=m.text)
    await state.set_state(FormAddPayment.date_payment)
    await m.answer(text=f'Напиши число оплаты\n'
                        '<i>(Только сам день)</i>')

@add_payment_router.message(FormAddPayment.date_payment)
async def accept_date(m: Message, state: FSMContext):
    date_pay = m.text
    if check_day_payment_format(date_pay):
        await state.update_data(date_payment=m.text)
        notices = await get_notice_user(m.from_user.id)
        list_notices = [notice['name_notice'] for notice in notices]
        await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
        await state.set_state(FormAddPayment.notice_payment)
    else:
        await m.answer(text='Вы ввели не корректное число, попробуйте еще раз')
        await state.set_state(FormAddPayment.date_payment)


@add_payment_router.message(FormAddPayment.notice_payment)
async def accept_notice(m: Message, state: FSMContext):
    if m.text == 'Добавить новое':
        await m.answer(text='Введите за сколько дней будет приходить уведомление\n\n'
                            '<i>Например - если нужно присылать за два дня, то вводите 2</i>', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormAddPayment.day_notice)
        return
    notice = await get_notice(m.from_user.id, m.text)
    if notice:
        info = await state.get_data()
        name_pay = info.get('name_payment')
        cost_pay = info.get('cost_payment')
        date_pay = info.get('date_payment')
        answer = await add_payment(m.from_user.id, notice.id, name_pay, int(cost_pay), int(date_pay))
        if answer:
            await m.answer(text='Вы успешно добавили платеж', reply_markup=ReplyKeyboardRemove())
        else:
            await m.answer(text='При создании произошла ошибка', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='Такого уведомления у вас нет, попробуйте еще раз')
        await state.set_state(FormAddPayment.notice_payment)
        return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
    
@add_payment_router.message(FormAddPayment.day_notice)
async def accept_day_notice(m: Message, state: FSMContext):
    if check_day_notice_format(m.text):
        await state.update_data(day_notice=m.text)
        await m.answer(text=f'Введите время уведомления в формате час:минуты\n\n'
                            f'<i>Например - {datetime.now().time().strftime("%H:%M")}</i>')
        await state.set_state(FormAddPayment.time_notice)
        return
    await m.answer(text='Не корректно указан день, попробуйте еще раз')
    await state.set_state(FormAddPayment.day_notice)


@add_payment_router.message(FormAddPayment.time_notice)
async def accept_time_notice(m: Message, state: FSMContext):
    if not check_time_format(m.text):
        await m.answer(text='Не корректно указано время, попробуйте еще раз')
        await state.set_state(FormAddPayment.time_notice)
        return
    time_notice = m.text
    info = await state.get_data()
    day_notice = info.get('day_notice')
    creator = 'user'
    answer = await add_notice(m.from_user.id, int(day_notice), time_notice, creator)
    if answer:
        notice = await get_notice(m.from_user.id, f'за {day_notice} д в {time_notice}')
        if notice:
            info = await state.get_data()
            name_pay = info.get('name_payment')
            cost_pay = info.get('cost_payment')
            date_pay = info.get('date_payment')
            answer = await add_payment(m.from_user.id, notice.id, name_pay, int(cost_pay), int(date_pay))
            if answer:
                await m.answer(text='Вы успешно добавили платеж', reply_markup=ReplyKeyboardRemove())
            else:
                await m.answer(text='При создании произошла ошибка', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='Такое уведомление уже есть')
        notices = await get_notice_user(m.from_user.id)
        list_notices = [notice['name_notice'] for notice in notices]
        await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
        await state.set_state(FormAddPayment.notice_payment)
        return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())