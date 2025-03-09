from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.db.Notice_db.add_notice_db import add_notice
from src.db.Notice_db.get_all_notices_person import get_notices_user
from src.db.Notice_db.get_notice_db import get_notice
from src.db.Payments.get_payment_db import get_payment
from src.db.Payments.delete_payment_db import delete_payment
from src.db.Payments.edit_payment_db import edit_date_payment
from src.db.models import Notice, Payment
from src.filters.all_avaiable_payment_filter import AllAvailablePaymentFilter
from src.filters.cost_payment_filter import CostPaymentFilter
from src.filters.day_payment_filter import DayPaymentFilter
from src.filters.exists_notice_filter import ExistsNoticeFilter
from src.filters.exists_payment_filter import ExistsPaymentFilter
from src.filters.not_none_filter import NotNoneFilter
from src.filters.time_notice_filter import TimeNoticeFilter
from src.handlers.Notice_hd.add_notice_hd import request_day_before
from src.keyboards.inline_kb.menu_kb import main_start_inline_kb
from src.keyboards.line_kb.utils_line_kb import kb_list_data, kb_edit_delete, kb_all_payment_data, kb_choice_notice
from src.states.all_states import FormEditPayment
from src.utils.view_info import view_info_payment

edit_payment_router = Router()


@edit_payment_router.callback_query(F.data == 'edit_payment_call', AllAvailablePaymentFilter())
async def call_edit_payment(call: CallbackQuery, state: FSMContext, bot: Bot, list_payments: list[dict]):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    list_payment = [payment['name_payment'] for payment in list_payments]
    await call.message.answer(text='Выберите платеж', reply_markup=kb_list_data(list_payment))
    await state.set_state(FormEditPayment.select_payment)


@edit_payment_router.message(FormEditPayment.select_payment, ExistsPaymentFilter())
async def accept_select_payment(m: Message, state: FSMContext, payment: Payment):
    await state.update_data(select_payment=m.text)
    text = await view_info_payment(m, payment)
    await m.answer(text=text)
    await m.answer(text='Что вы хотите сделать?', reply_markup=kb_edit_delete())
    await state.set_state(FormEditPayment.select_act)


@edit_payment_router.message(FormEditPayment.select_act, F.text == 'Удалить')
async def accept_select_act(m: Message, state: FSMContext):
    await m.answer(text='Вы точно хотите удалить платеж?\n'
                        '<i>(Для подтверждения введите "да"</i>)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FormEditPayment.verif_delete)


@edit_payment_router.message(FormEditPayment.verif_delete, F.text.lower() == 'да')
async def check_verif_delete(m: Message, state: FSMContext):
    data = await state.get_data()
    payment = data.get('select_payment')
    answer = await delete_payment(m.from_user.id, payment)
    if answer:
        await m.answer(text='Вы успешно удалил платеж')
    else:
        await m.answer(text='При удаление произошла ошибка')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.select_act, F.text == 'Изменить')
async def request_select_edit_data(m: Message, state: FSMContext):
    await m.answer(text='Выберете что хотите изменить', reply_markup=kb_all_payment_data())
    await state.set_state(FormEditPayment.select_edit_data)


@edit_payment_router.message(FormEditPayment.select_edit_data,
                             F.text.in_(['Название', 'Стоимость', 'День оплаты', 'Уведомление']))
async def accept_select_edit_data(m: Message, state: FSMContext):
    await state.update_data(select_edit_data=m.text)
    if m.text == 'Название':
        await m.answer(text='Введите новое название', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_name_payment)
    elif m.text == 'Стоимость':
        await m.answer(text='Введите новую стоимость', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_cost_payment)
    elif m.text == 'День оплаты':
        await m.answer(text='Введите новый день оплаты', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_day_payment)
    elif m.text == 'Уведомление':
        await request_notice(m, state)


async def request_notice(m: Message, state: FSMContext):
    answer = await get_notices_user(m.from_user.id)
    list_notices = [notice['name_notice'] for notice in answer]
    await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
    await state.set_state(FormEditPayment.new_notice_payment)


@edit_payment_router.message(FormEditPayment.new_name_payment, NotNoneFilter())
async def accept_new_name_payment(m: Message, state: FSMContext):
    # собираем данные
    new_name = m.text
    payment = await get_payment(m.from_user.id, new_name)
    if payment:
        await m.answer(text='Платеж с таким именем уже есть, попробуйте еще раз')
        await state.set_state(FormEditPayment.new_name_payment)
        return
    await update_payment_in_db(m, state, new_name)


@edit_payment_router.message(FormEditPayment.new_cost_payment, CostPaymentFilter())
async def accept_new_cost_payment(m: Message, state: FSMContext):
    new_cost = int(m.text)
    await update_payment_in_db(m, state, new_cost)


@edit_payment_router.message(FormEditPayment.new_day_payment, DayPaymentFilter())
async def accept_new_cost_payment(m: Message, state: FSMContext):
    new_day = int(m.text)
    await update_payment_in_db(m, state, new_day)


@edit_payment_router.message(FormEditPayment.new_notice_payment, ExistsNoticeFilter())
async def accept_notice(m: Message, state: FSMContext, notice: Notice):
    await update_payment_in_db(m, state, notice.id)


@edit_payment_router.message(FormEditPayment.new_notice_payment, F.text == 'Добавить новое')
async def accept_new_notice_payment(m: Message, state: FSMContext):
    await state.update_data(edit_payment=True)
    await request_day_before(m, state)


@edit_payment_router.message(FormEditPayment.time_notice, TimeNoticeFilter())
async def accept_time_notice(m: Message, state: FSMContext):
    time_notice = m.text
    data = await state.get_data()
    day_notice = data.get('day_notice')
    creator = 'user'
    answer = await add_notice(m.from_user.id, int(day_notice), time_notice, creator)
    if answer:
        notice = await get_notice(m.from_user.id, f'за {day_notice} д в {time_notice}')
        await update_payment_in_db(m, state, notice.id)
    else:
        await m.answer(text='Такое уведомление уже есть')
        await request_notice(m, state)


async def update_payment_in_db(m: Message, state: FSMContext, new_value):
    data = await state.get_data()
    name_payment = data.get('select_payment')
    select_edit_data = data.get('select_edit_data')
    # изменяем значения
    answer = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, new_value)
    if answer:
        await m.answer(text='Вы успешно изменили данные', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='При изменении произошла ошибка', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


# Ниже ловим ошибки при вводе


@edit_payment_router.callback_query(F.data == 'edit_payment_call')
async def error_call_edit_payment(call: CallbackQuery):
    await call.message.answer(text='У вас нет ни одного платежа')
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.verif_delete)
async def check_verif_delete(m: Message, state: FSMContext):
    await m.answer(text='Удаление отменено')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.select_payment)
@edit_payment_router.message(FormEditPayment.select_act)
@edit_payment_router.message(FormEditPayment.select_edit_data)
@edit_payment_router.message(FormEditPayment.new_name_payment)
@edit_payment_router.message(FormEditPayment.new_cost_payment)
@edit_payment_router.message(FormEditPayment.new_day_payment)
@edit_payment_router.message(FormEditPayment.new_notice_payment)
@edit_payment_router.message(FormEditPayment.time_notice)
async def accept_select_payment(m: Message, state: FSMContext):
    await m.answer(text='Не корректные данные, попробуйте еще раз')
    current_state = await state.get_state()
    await state.set_state(current_state)
