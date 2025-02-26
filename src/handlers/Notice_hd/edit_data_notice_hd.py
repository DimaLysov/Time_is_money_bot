from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.db.Notice_db.delete_notice_db import delete_notice
from src.db.Notice_db.edit_notice_data_db import edit_notice_data
from src.db.Notice_db.get_all_notice_person import get_notice_user
from src.db.Notice_db.get_notice_db import get_notice
from src.keyboards.inline_kb.main_kb import main_start_inline_kb
from src.keyboards.line_kb import kb_list_data, kb_edit_delete, kb_all_notice_data
from src.utils.check_fn import check_dey_format, check_time_format

edit_notice_router = Router()


class FormEditNotice(StatesGroup):
    select_notice = State()
    select_act = State()
    select_edit_data = State()
    verif_delete = State()
    new_value = State()


@edit_notice_router.callback_query(F.data == 'edit_notice_call')
async def call_edit_notice(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    answer = await get_notice_user(call.from_user.id)
    if answer:
        list_notice = [notice['name_notice'] for notice in answer]
        await call.message.answer(text='Выберете уведомление', reply_markup=kb_list_data(list_notice))
        await state.set_state(FormEditNotice.select_notice)
    else:
        await call.message.answer(text='У вас нет ни одного уведомления')
        await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_notice_router.message(FormEditNotice.select_notice)
async def accept_select_notice(m: Message, state: FSMContext):
    notice = await get_notice(m.from_user.id, m.text)
    if notice:
        if notice.creator == 'bot':
            await state.update_data(select_edit_data='Сделать активным')
            await state.update_data(select_notice=m.text)
            await m.answer(text='У стандартного уведомления можно изменить статус\n'
                                'Для подтверждения введите "да"', reply_markup=ReplyKeyboardRemove())
            await state.set_state(FormEditNotice.new_value)
        else:
            await state.update_data(select_notice=m.text)
            await m.answer(text='Что вы хотите сделать?', reply_markup=kb_edit_delete())
            await state.set_state(FormEditNotice.select_act)
    else:
        await m.answer(text='Такого уведомления у вас нет, попробуйте еще раз')
        await state.set_state(FormEditNotice.select_notice)


@edit_notice_router.message(FormEditNotice.select_act)
async def accept_select_act(m: Message, state: FSMContext):
    if m.text == 'Изменить':
        await m.answer(text='Выберете что хотите изменить', reply_markup=kb_all_notice_data())
        await state.set_state(FormEditNotice.select_edit_data)
    elif m.text == 'Удалить':
        await m.answer(
            text='Вы точно хотите удалить уведомление. У всех платежей с данным уведомлением установиться стандартное уведомление\n'
                 '<i>Для подтверждения введите "да"</i>', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditNotice.verif_delete)
    else:
        await m.answer(text='Я не знаю такой команды, попробуйте еще раз')
        await state.set_state(FormEditNotice.select_act)


@edit_notice_router.message(FormEditNotice.verif_delete)
async def accept_verif_delete(m: Message, state: FSMContext):
    if m.text.lower() == 'да':
        date = await state.get_data()
        name_notice = date.get('select_notice')
        answer = await delete_notice(m.from_user.id, name_notice)
        if answer:
            await m.answer(text='Вы успешно удалил уведомление')
        else:
            await m.answer(text='При удаление произошла ошибка')
    else:
        await m.answer(text='Удаление отменено')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_notice_router.message(FormEditNotice.select_edit_data)
async def accept_select_edit_data(m: Message, state: FSMContext):
    await state.update_data(select_edit_data=m.text)
    if m.text == 'За сколько дней':
        await m.answer(text='Введите за сколько дней', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditNotice.new_value)
    elif m.text == 'Время':
        await m.answer(text='Введите новое время', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditNotice.new_value)
    elif m.text == 'Сделать активным':
        await m.answer(text='Для подтверждения введите "да"', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FormEditNotice.new_value)
    else:
        await m.answer(text='Не известные данные, попробуйте еще раз')
        await state.set_state(FormEditNotice.select_edit_data)


@edit_notice_router.message(FormEditNotice.new_value)
async def accept_new_value(m: Message, state: FSMContext):
    # собираем данные
    new_value = m.text
    data = await state.get_data()
    name_notice = data.get('select_notice')
    select_edit_data = data.get('select_edit_data')
    answer = False
    # проверка данных
    if select_edit_data == 'За сколько дней':
        if check_dey_format(new_value):
            new_value = int(new_value)
            answer = await edit_notice_data(m.from_user.id, name_notice, select_edit_data, new_value)
        else:
            await m.answer(text='Данные введены не корректно, попробуете еще раз')
            await state.set_state(FormEditNotice.new_value)
            return
    elif select_edit_data == 'Время':
        if check_time_format(new_value):
            answer = await edit_notice_data(m.from_user.id, name_notice, select_edit_data, new_value)
        else:
            await m.answer(text='Данные введены не корректно, попробуете еще раз')
            await state.set_state(FormEditNotice.new_value)
            return
    elif select_edit_data == 'Сделать активным':
        if new_value.lower() == 'да':
            new_value = True
            answer = await edit_notice_data(m.from_user.id, name_notice, select_edit_data, new_value)
    # вывод
    if answer:
        await m.answer(text='Вы успешно изменили данные')
    else:
        await m.answer(text='Изменения не произошли')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())



