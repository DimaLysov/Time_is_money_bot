from aiogram.fsm.state import StatesGroup, State


class FormAddNotice(StatesGroup):
    add_payment = State()
    edit_payment = State()
    day_notice = State()
    time_notice = State()


class FormEditNotice(StatesGroup):
    select_notice = State()
    select_act = State()
    select_edit_data = State()
    verif_delete = State()
    new_day_before = State()
    new_time_notice = State()


class FormAddPayment(StatesGroup):
    name_payment = State()
    cost_payment = State()
    day_payment = State()
    notice_payment = State()
    time_notice = State()


class FormEditPayment(StatesGroup):
    select_payment = State()
    select_act = State()
    select_edit_data = State()
    verif_delete = State()
    new_name_payment = State()
    new_cost_payment = State()
    new_day_payment = State()
    new_notice_payment = State()
    time_notice = State()
