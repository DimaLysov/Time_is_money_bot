from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from datetime import date

from src.create_bot import bot
from src.db.Payments.add_payments_db import add_payment
from src.keyboards.inline_kb.main_kb import main_start_inline_kb
from src.utils.check_fn import check_date_format

add_payment_router = Router()


class FormAddPayment(StatesGroup):
    name_payment = State()
    cost_payment = State()
    date_payment = State()

@add_payment_router.callback_query(F.data == 'new_payment_call')
async def call_add_payment(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text='Введите название нового платежа')
    await state.set_state(FormAddPayment.name_payment)

@add_payment_router.message(FormAddPayment.name_payment)
async def accept_name_payment(m: Message, state: FSMContext):
    await state.update_data(name_payment=m.text)
    await state.set_state(FormAddPayment.cost_payment)
    await m.answer(text='Введи цену вашей подписки')


@add_payment_router.message(FormAddPayment.cost_payment)
async def accept_cost(m: Message, state: FSMContext):
    await state.update_data(cost_payment=m.text)
    await state.set_state(FormAddPayment.date_payment)

    await m.answer(text=f'Напиши число оплаты')

@add_payment_router.message(FormAddPayment.date_payment)
async def accept_date(m: Message, state: FSMContext):
    date_pay = m.text
    if not check_date_format(date_pay):
        await m.answer(text='Вы ввели не корректное число, попробуйте еще раз')
        await state.set_state(FormAddPayment.date_payment)
    info = await state.get_data()
    name_pay = info.get('name_payment')
    cost_pay = info.get('cost_payment')
    answer = await add_payment(m.from_user.id, name_pay, int(cost_pay), int(date_pay))
    if answer:
        await m.answer(text='Вы успешно добавили платеж')
    else:
        await m.answer(text='Платеж с таким названием у вас уже есть')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())