from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.create_bot import bot
from src.keyboards.inline_kb.main_kb import main_start_inline_kb

clear_router = Router()

@clear_router.message(Command('clear'))
async def cmd_clear(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(text='Выход...', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(m.from_user.id, m.message_id+1)
    await m.answer(text='Панель навигации', reply_markup=main_start_inline_kb())