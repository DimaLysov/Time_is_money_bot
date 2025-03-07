from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.db.Notice_db.add_notice_db import add_notice
from src.db.Notice_db.get_all_notices_person import get_notices_user
from src.db.Notice_db.get_notice_db import get_notice
from src.db.Payments.get_payment_db import get_payment
from src.db.Payments.delete_payment_db import delete_payment
from src.db.Payments.edit_payment_db import edit_date_payment
from src.db.Payments.get_all_payment_person_db import get_payments_user
from src.keyboards.inline_kb.menu_kb import main_start_inline_kb
from src.keyboards.line_kb.utils_line_kb import kb_list_data, kb_edit_delete, kb_all_payment_data, kb_choice_notice
from src.utils.check_fn import check_day_payment_format, check_time_format

edit_payment_router = Router()


class FormEditPayment(StatesGroup):
    select_payment = State()
    select_act = State()
    select_edit_data = State()
    verif_delete = State()
    new_name_payment = State()
    new_cost_payment = State()
    new_date_payment = State()
    new_notice_payment = State()
    day_notice = State()
    time_notice = State()


@edit_payment_router.callback_query(F.data == 'edit_payment_call')
async def call_edit_payment(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_payments_user(call.from_user.id)
    if answer:
        list_payment = [payment['name_payment'] for payment in answer]
        await call.message.answer(text='Выберите платеж', reply_markup=kb_list_data(list_payment))
        await state.set_state(FormEditPayment.select_payment)
    else:
        await call.message.answer(text='У вас нет ни одного платежа')
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.select_payment)
async def accept_select_payment(m: Message, state: FSMContext):
    payment = await get_payment(m.from_user.id, m.text)
    if payment:
        await state.update_data(select_payment=m.text)
        await m.answer(text='Что вы хотите сделать?', reply_markup=kb_edit_delete())
        await state.set_state(FormEditPayment.select_act)
    else:
        await m.answer(text='Такого платежа у вас нет, попробуйте еще раз')
        await state.set_state(FormEditPayment.select_payment)


@edit_payment_router.message(FormEditPayment.select_act)
async def accept_select_act(m: Message, state: FSMContext):
    if m.text == 'Изменить':
        await m.answer(text='Выберете что хотите изменить', reply_markup=kb_all_payment_data())
        await state.set_state(FormEditPayment.select_edit_data)
    elif m.text == 'Удалить':
        await m.answer(text='Вы точно хотите удалить платеж?\n'
                            '<i>(Для подтверждения введите "да"</i>)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.verif_delete)
    else:
        await m.answer(text='Такое я не могу сделать, повторите выбор')
        await state.set_state(FormEditPayment.select_act)


@edit_payment_router.message(FormEditPayment.verif_delete)
async def check_verif_delete(m: Message, state: FSMContext):
    if m.text.lower() == 'да':
        data = await state.get_data()
        payment = data.get('select_payment')
        answer = await delete_payment(m.from_user.id, payment)
        if answer:
            await m.answer(text='Вы успешно удалил платеж')
        else:
            await m.answer(text='При удаление произошла ошибка')
    else:
        await m.answer(text='Удаление отменено')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.select_edit_data)
async def accept_select_edit_data(m: Message, state: FSMContext):
    await state.update_data(select_edit_data=m.text)
    if m.text == 'Название':
        await m.answer(text='Введите новое название', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_name_payment)
    elif m.text == 'Стоимость':
        await m.answer(text='Введите новую стоимость', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_cost_payment)
    elif m.text == 'Дата оплаты':
        await m.answer(text='Введите новую дату оплаты', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.new_date_payment)
    elif m.text == 'Уведомление':
        answer = await get_notices_user(m.from_user.id)
        list_notices = [notice['name_notice'] for notice in answer]
        await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
        await state.set_state(FormEditPayment.new_notice_payment)
    else:
        await m.answer(text='Не известные данные, попробуйте еще раз')
        await state.set_state(FormEditPayment.select_edit_data)


@edit_payment_router.message(FormEditPayment.new_name_payment)
async def accept_new_name_payment(m: Message, state: FSMContext):
    # собираем данные
    new_name = m.text
    payment = await get_payment(m.from_user.id, new_name)
    if payment:
        await m.answer(text='Платеж с таким именем уже есть, попробуйте еще раз')
        await state.set_state(FormEditPayment.new_name_payment)
        return
    data = await state.get_data()
    name_payment = data.get('select_payment')
    select_edit_data = data.get('select_edit_data')
    # изменяем значения
    answer = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, new_name)
    if answer:
        await m.answer(text='Вы успешно изменили имя')
    else:
        await m.answer(text='При изменении произошла ошибка')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.new_cost_payment)
async def accept_new_cost_payment(m: Message, state: FSMContext):
    # проверка
    if not m.text.isdigit():
        await m.answer(text='Некорректно указана цена, попробуйте еще раз')
        await state.set_state(FormEditPayment.new_cost_payment)
        return
    # собираем данные
    new_cost = int(m.text)
    data = await state.get_data()
    name_payment = data.get('select_payment')
    select_edit_data = data.get('select_edit_data')
    # изменяем значения
    answer = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, new_cost)
    if answer:
        await m.answer(text='Вы успешно изменили стоимость')
    else:
        await m.answer(text='При изменении произошла ошибка')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.new_date_payment)
async def accept_new_cost_payment(m: Message, state: FSMContext):
    # проверка
    if not check_day_payment_format(m.text):
        await m.answer(text='Некорректно указана дата, попробуйте еще раз')
        await state.set_state(FormEditPayment.new_date_payment)
        return
    # собираем данные
    new_date = int(m.text)
    data = await state.get_data()
    name_payment = data.get('select_payment')
    select_edit_data = data.get('select_edit_data')
    # изменяем значения
    answer = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, new_date)
    if answer:
        await m.answer(text='Вы успешно изменили дату')
    else:
        await m.answer(text='При изменении произошла ошибка')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.new_notice_payment)
async def accept_new_notice_payment(m: Message, state: FSMContext):
    if m.text == 'Добавить новое':
        await m.answer(text='Введите за сколько дней будет приходить уведомление\n\n'
                            '<i>Например - если нужно присылать за два дня, то вводите 2</i>',
                       reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditPayment.day_notice)
        return
    notice = await get_notice(m.from_user.id, m.text)
    # проверка
    if not notice:
        await m.answer(text='У вас нет такого уведомления, попробуйте еще раз')
        await state.set_state(FormEditPayment.new_notice_payment)
        return
    # собираем данные
    data = await state.get_data()
    name_payment = data.get('select_payment')
    select_edit_data = data.get('select_edit_data')
    # изменяем значения
    answer = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, notice.id)
    if answer:
        await m.answer(text='Вы успешно изменили уведомление', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='При изменении произошла ошибка', reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_payment_router.message(FormEditPayment.day_notice)
async def accept_day_notice(m: Message, state: FSMContext):
    if m.text.isdigit():
        if int(m.text) < 32:
            await state.update_data(day_notice=m.text)
            await m.answer(text=f'Введите время уведомления в формате час:минуты\n\n'
                                f'<i>Например - {datetime.now().time().strftime("%H:%M")}</i>')
            await state.set_state(FormEditPayment.time_notice)
            return
    await m.answer(text='Не корректно указан день, попробуйте еще раз')
    await state.set_state(FormEditPayment.day_notice)


@edit_payment_router.message(FormEditPayment.time_notice)
async def accept_time_notice(m: Message, state: FSMContext):
    if not check_time_format(m.text):
        await m.answer(text='Не корректно указано время, попробуйте еще раз')
        await state.set_state(FormEditPayment.time_notice)
        return
    time_notice = m.text
    data = await state.get_data()
    day_notice = data.get('day_notice')
    creator = 'user'
    answer_1 = await add_notice(m.from_user.id, int(day_notice), time_notice, creator)
    if answer_1:
        notice = await get_notice(m.from_user.id, f'за {day_notice} д в {time_notice}')
        name_payment = data.get('select_payment')
        select_edit_data = data.get('select_edit_data')
        answer_2 = await edit_date_payment(m.from_user.id, name_payment, select_edit_data, notice.id)
        if answer_2:
            await m.answer(text='Вы успешно изменили уведомление', reply_markup=ReplyKeyboardRemove())
        else:
            await m.answer(text='При изменении произошла ошибка', reply_markup=ReplyKeyboardRemove())
    else:
        await m.answer(text='Такое уведомление уже есть')
        answer_3 = await get_notices_user(m.from_user.id)
        list_notices = [notice['name_notice'] for notice in answer_3]
        await m.answer(text='Выберете уведомление', reply_markup=kb_choice_notice(list_notices))
        await state.set_state(FormEditPayment.new_notice_payment)
        return
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())
