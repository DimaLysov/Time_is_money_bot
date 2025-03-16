from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.all_time_zone import rus_time_zone


def main_start_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Платежи', callback_data='main_payment'),
         InlineKeyboardButton(text='Уведомления', callback_data='main_notice')],
        [InlineKeyboardButton(text='Часовой пояс', callback_data='time_zone'),
         InlineKeyboardButton(text='Инструкция ⚙️', callback_data='main_setting')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def payments_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Добавить платеж', callback_data='new_payment_call'),
         InlineKeyboardButton(text='Все платежи', callback_data='view_payment_call')],
        [InlineKeyboardButton(text='Изменить данные', callback_data='edit_payment_call'),
         InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def notice_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Добавить уведомление', callback_data='new_notice_call'),
         InlineKeyboardButton(text='Все уведомления', callback_data='view_notice_call')],
        [InlineKeyboardButton(text='Изменить данные', callback_data='edit_notice_call'),
         InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def time_zone_kb():
    builder = InlineKeyboardBuilder()
    for time in rus_time_zone:
        builder.row(InlineKeyboardButton(text=f'{time}', callback_data=f'tz_{time}'))
    return builder.as_markup()

def yes_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Да', callback_data='yes_call'),
         InlineKeyboardButton(text='Нет', callback_data='no_call')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)