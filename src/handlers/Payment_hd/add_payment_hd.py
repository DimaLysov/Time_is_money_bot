from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.Notice_db.add_notice_db import add_notice
from db.Notice_db.get_all_notices_person import get_notices_user
from db.Notice_db.get_notice_db import get_notice
from db.Payments.add_payments_db import add_payment
from db.models import Notice
from filters.cost_payment_filter import CostPaymentFilter
from filters.day_payment_filter import DayPaymentFilter
from filters.exists_notice_filter import ExistsNoticeFilter
from filters.exists_payment_filter import ExistsPaymentFilter
from filters.not_none_filter import NotNoneFilter
from filters.time_notice_filter import TimeNoticeFilter
from handlers.Notice_hd.add_notice_hd import request_day_before
from keyboards.inline_kb.menu_kb import main_start_inline_kb
from keyboards.line_kb.utils_line_kb import kb_choice_notice
from states.all_states import FormAddPayment

add_payment_router = Router()


@add_payment_router.callback_query(F.data == 'new_payment_call')
async def call_add_payment(call: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Введите название нового платежа')
    await state.set_state(FormAddPayment.name_payment)


@add_payment_router.message(FormAddPayment.name_payment, NotNoneFilter(), ~ExistsPaymentFilter())
async def accept_name_payment(m: Message, state: FSMContext):
    await state.update_data(name_payment=m.text)
    await state.set_state(FormAddPayment.cost_payment)
    await m.answer(text='Введи цену вашей подписки (в рублях)')


@add_payment_router.message(FormAddPayment.cost_payment, CostPaymentFilter())
async def accept_cost(m: Message, state: FSMContext):
    await state.update_data(cost_payment=m.text)
    await state.set_state(FormAddPayment.day_payment)
    await m.answer(text=f'Напиши число оплаты\n'
                        '<i>(Только сам день)</i>')


@add_payment_router.message(FormAddPayment.day_payment, DayPaymentFilter())
async def accept_day_payment(m: Message, state: FSMContext):
    await state.update_data(day_payment=m.text)
    await request_notice(m, state)


async def request_notice(m: Message, state: FSMContext):
    notices = await get_notices_user(m.from_user.id)
    list_notices = [notice['name_notice'] for notice in notices]
    await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
    await state.set_state(FormAddPayment.notice_payment)


@add_payment_router.message(FormAddPayment.notice_payment, ExistsNoticeFilter())
async def accept_notice(m: Message, state: FSMContext, notice: Notice):
    await add_payment_in_db(m, state, notice)


@add_payment_router.message(FormAddPayment.notice_payment, F.text == 'Добавить новое')
async def add_new_notice(m: Message, state: FSMContext):
    await state.update_data(add_payment=True)
    await request_day_before(m, state)


@add_payment_router.message(FormAddPayment.time_notice, TimeNoticeFilter())
async def accept_time_notice(m: Message, state: FSMContext):
    time_notice = m.text
    info = await state.get_data()
    day_notice = info.get('day_notice')
    creator = 'user'
    answer = await add_notice(m.from_user.id, int(day_notice), time_notice, creator)
    if not answer:
        await m.answer(text='Такое уведомление уже есть')
        await request_notice(m, state)
        return
    notice = await get_notice(m.from_user.id, f'за {day_notice} д в {time_notice}')
    await add_payment_in_db(m, state, notice)


async def add_payment_in_db(m: Message, state: FSMContext, notice: Notice):
    info = await state.get_data()
    name_pay = info.get('name_payment')
    cost_pay = info.get('cost_payment')
    day_pay = info.get('day_payment')
    answer = await add_payment(m.from_user.id, notice.id, name_pay, int(cost_pay), int(day_pay))
    if answer:
        await m.answer(text='Вы успешно добавили платеж', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='При создании произошла ошибка', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


# Ниже ловим ошибки при вводе

@add_payment_router.message(FormAddPayment.name_payment, ExistsPaymentFilter())
async def error_accept_name_payment(m: Message, state: FSMContext):
    await m.answer(text='Платеж с таким названием уже есть, попробуйте еще раз')
    await state.set_state(FormAddPayment.name_payment)


@add_payment_router.message(FormAddPayment.name_payment)
@add_payment_router.message(FormAddPayment.cost_payment)
@add_payment_router.message(FormAddPayment.day_payment)
@add_payment_router.message(FormAddPayment.notice_payment)
@add_payment_router.message(FormAddPayment.time_notice)
async def error_data(m: Message, state: FSMContext):
    await m.answer(text='Не корректные данные, попробуйте еще раз')
    current_state = await state.get_state()
    await state.set_state(current_state)
