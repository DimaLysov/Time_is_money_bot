from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_list_data(list_data):
    kb_list = []
    for item in range(1, len(list_data), 2):
        kb_list.append([KeyboardButton(text=list_data[item - 1]), KeyboardButton(text=list_data[item])])
    if len(list_data) % 2 != 0:
        kb_list.append([KeyboardButton(text=list_data[-1])])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Выберите:')
    return keyboard


def kb_choice_notice(list_data):
    kb_list = []
    for item in range(1, len(list_data), 2):
        kb_list.append([KeyboardButton(text=list_data[item - 1]), KeyboardButton(text=list_data[item])])
    if len(list_data) % 2 != 0:
        kb_list.append([KeyboardButton(text=list_data[-1])])
    kb_list.append([KeyboardButton(text='Добавить новое')])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Выберите уведомление')
    return keyboard


def kb_edit_delete():
    kb_list = [[KeyboardButton(text='Изменить'), KeyboardButton(text='Удалить')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Выберите, что хотите сделать')
    return keyboard


def kb_all_payment_data():
    kb_list = [[KeyboardButton(text='Название'), KeyboardButton(text='Стоимость')],
               [KeyboardButton(text='Дата оплаты'), KeyboardButton(text='Уведомление')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Выберите, что хотите изменить')
    return keyboard


def kb_all_notice_data():
    kb_list = [[KeyboardButton(text='За сколько дней'), KeyboardButton(text='Время')],
               [KeyboardButton(text='Сделать активным')]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, input_field_placeholder='Выберите, что хотите изменить')
    return keyboard
