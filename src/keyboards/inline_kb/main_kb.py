from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_start_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Мои платежи', callback_data='main_payment'),
         InlineKeyboardButton(text='Настройка уведомлений', callback_data='main_notice')],
        [InlineKeyboardButton(text='Инструкция ⚙️', callback_data='main_setting')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def payments_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Добавить платеж', callback_data='-'),
         InlineKeyboardButton(text='Мои платежи', callback_data='-')],
        [InlineKeyboardButton(text='Изменить данные', callback_data='-'),
         InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def notice_inline_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text='Добавить уведомление', callback_data='-'),
         InlineKeyboardButton(text='Мои уведомления', callback_data='-')],
        [InlineKeyboardButton(text='Изменить данные', callback_data='-'),
         InlineKeyboardButton(text='В главное меню ⬅️', callback_data='back_main')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
