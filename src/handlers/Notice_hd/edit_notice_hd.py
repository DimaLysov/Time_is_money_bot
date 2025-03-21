from datetime import datetime

import pytz
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.Notice_db.delete_notice_db import delete_notice
from db.Notice_db.edit_notice_data_db import edit_notice_data
from db.Notice_db.get_notice_db import get_notice
from db.Users.get_user_db import get_user
from db.models import Notice
from filters.all_available_notices_filter import AllAvailableNoticeFilter
from filters.day_before_fillter import DayBeforeFilter
from filters.exists_notice_filter import ExistsNoticeFilter
from filters.time_notice_filter import TimeNoticeFilter
from keyboards.inline_kb.menu_kb import main_start_inline_kb, yes_no_kb
from keyboards.line_kb.utils_line_kb import kb_list_data, kb_edit_delete, kb_all_notice_data
from states.all_states import FormEditNotice
from utils.all_time_zone import rus_time_zone

edit_notice_router = Router()


@edit_notice_router.callback_query(F.data == 'edit_notice_call', AllAvailableNoticeFilter())
async def call_edit_notice(call: CallbackQuery, state: FSMContext, bot: Bot, list_notices: list[dict]):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    all_name_notices = [notice['name_notice'] for notice in list_notices if notice['creator'] != 'bot']
    await call.message.answer(text='Выберете уведомление', reply_markup=kb_list_data(all_name_notices))
    await state.set_state(FormEditNotice.select_notice)


@edit_notice_router.message(FormEditNotice.select_notice, ExistsNoticeFilter())
async def request_select_act(m: Message, state: FSMContext, notice: Notice):
    if notice.creator != 'bot':
        await state.update_data(select_notice=m.text)
        await m.answer(text='Что вы хотите сделать?', reply_markup=kb_edit_delete())
        await state.set_state(FormEditNotice.select_act)
    else:
        await m.answer(text='Вы не можете изменять стандартное уведомление')
        await state.set_state(FormEditNotice.select_notice)


@edit_notice_router.message(FormEditNotice.select_act, F.text == 'Удалить')
async def accept_delete_act(m: Message):
    await m.answer(text='Вы точно хотите удалить уведомление?\n\n'
                        'У всех платежей с данным уведомлением установиться стандартное уведомление',
                   reply_markup=ReplyKeyboardRemove())
    await m.answer(text='Подтверждение', reply_markup=yes_no_kb('edit_notice_hd.py'))


@edit_notice_router.callback_query(F.data == 'yes_call_edit_notice_hd.py')
async def accept_verif_delete(call: CallbackQuery, state: FSMContext):
    date = await state.get_data()
    name_notice = date.get('select_notice')
    answer = await delete_notice(call.from_user.id, name_notice)
    if answer:
        await call.message.answer(text='Вы успешно удалили уведомление')
    else:
        await call.message.answer(text='При удаление произошла ошибка')
    await state.clear()
    await call.message.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


@edit_notice_router.callback_query(F.data == 'no_call_edit_notice_hd.py')
async def undo_delete(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text='Удаление отклонено')
    await call.message.answer(text='Что вы хотите сделать?', reply_markup=kb_edit_delete())
    await state.set_state(FormEditNotice.select_act)


@edit_notice_router.message(FormEditNotice.select_act, F.text == 'Изменить')
async def accept_edit_act(m: Message, state: FSMContext):
    await m.answer(text='Выберете что хотите изменить', reply_markup=kb_all_notice_data())
    await state.set_state(FormEditNotice.select_edit_data)


@edit_notice_router.message(FormEditNotice.select_edit_data, F.text == 'За сколько дней')
async def request_new_day_before(m: Message, state: FSMContext):
    await state.update_data(select_edit_data=m.text)
    await m.answer(text='Введите за сколько дней будет приходить уведомление\n\n'
                        '<i>Например - если нужно присылать за два дня, то вводите 2</i>',
                   reply_markup=ReplyKeyboardRemove())
    await state.set_state(FormEditNotice.new_day_before)


@edit_notice_router.message(FormEditNotice.new_day_before, DayBeforeFilter())
async def accept_new_day_before(m: Message, state: FSMContext):
    data = await state.get_data()
    name_edit_notice = data.get('select_notice')
    new_day_before = int(m.text)
    notice = await get_notice(m.from_user.id, f'за {new_day_before}{name_edit_notice[4:]}')
    if notice:
        await m.answer(text='Такое уведомление уже есть, попробуйте еще раз')
        await state.set_state(FormEditNotice.new_day_before)
    else:
        await update_notice(m, state, new_day_before)


@edit_notice_router.message(FormEditNotice.select_edit_data, F.text == 'Время')
async def request_new_time_notice(m: Message, state: FSMContext):
    await state.update_data(select_edit_data=m.text)
    user = await get_user(m.from_user.id)
    await m.answer(text=f'Введите время уведомления в формате час:минуты\n\n'
                        f'<i>Например - {datetime.now(pytz.timezone(rus_time_zone[user.time_zone])).time().strftime("%H:%M")}</i>',
                   reply_markup=ReplyKeyboardRemove())
    await state.set_state(FormEditNotice.new_time_notice)


@edit_notice_router.message(FormEditNotice.new_time_notice, TimeNoticeFilter())
async def accept_new_time_notice(m: Message, state: FSMContext):
    data = await state.get_data()
    name_edit_notice = data.get('select_notice')
    new_time_notice = m.text
    notice = await get_notice(m.from_user.id, f'{name_edit_notice[:8]} {new_time_notice}')
    if notice:
        await m.answer(text='Такое уведомление уже есть, попробуйте еще раз')
        await state.set_state(FormEditNotice.new_time_notice)
    else:
        await update_notice(m, state, new_time_notice)


async def update_notice(m: Message, state: FSMContext, new_value):
    data = await state.get_data()
    name_edit_notice = data.get('select_notice')
    select_edit_data = data.get('select_edit_data')
    answer = await edit_notice_data(m.from_user.id, name_edit_notice, select_edit_data, new_value)
    if answer:
        await m.answer(text='Вы успешно изменили данные')
    else:
        await m.answer(text='Изменения не произошли')
    await state.clear()
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())


# Ниже ловим ошибки при вводе

@edit_notice_router.callback_query(F.data == 'edit_notice_call')
async def error_call_edit_notice(call: CallbackQuery):
    await call.message.answer(text='У вас нет ни одного уведомления')


@edit_notice_router.message(FormEditNotice.select_notice)
@edit_notice_router.message(FormEditNotice.select_act)
@edit_notice_router.message(FormEditNotice.select_edit_data)
@edit_notice_router.message(FormEditNotice.new_day_before)
@edit_notice_router.message(FormEditNotice.new_time_notice)
async def input_error(m: Message, state: FSMContext):
    await m.answer(text='Данные не соответствуют ожидаемому формату, попробуйте еще раз')
    current_state = await state.get_state()
    await state.set_state(current_state)
