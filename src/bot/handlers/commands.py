from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from create_bot import bot
# from handlers.time_zone_hd import request_time_zone
from keyboards.inline_kb.menu_kb import main_start_inline_kb
from requests.user import create_user

commands_router = Router()

@commands_router.message(CommandStart())
async def cmd_start(m: Message, state: FSMContext):
    await state.clear()
    answer = await create_user(m.from_user.id, m.from_user.username)
    await m.answer(text='Добро пожаловать.\n\n'
                        'Данный бот поможет вам своевременно оплачивать ваши ежемесячные подписки и другие платежи\n\n'
                        'Чтобы открыть меню бота нажмите сюда ️ 👉 <b>/menu</b>\n\n')
    # if answer:
    #     await request_time_zone(m)


@commands_router.message(Command('menu'))
async def cmd_menu(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(text='Выход...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(m.from_user.id, m.message_id + 1)
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())