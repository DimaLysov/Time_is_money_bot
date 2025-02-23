from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_start_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Мои платежи', callback_data='main_payment'),
         InlineKeyboardButton(text='Мои уведомления', callback_data='main_notice')],
        [InlineKeyboardButton(text='Инструкция ⚙️', callback_data='main_setting')]
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
         InlineKeyboardButton(text='Все уведомления', callback_data='-')],
        [InlineKeyboardButton(text='Изменить данные', callback_data='-'),
         InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
