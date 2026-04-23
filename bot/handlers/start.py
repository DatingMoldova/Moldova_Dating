from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.db import get_user
from bot.handlers.register import Reg

router = Router()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    print("START WORKING")

    user = get_user(message.from_user.id)

    if user:
        from bot.keyboards.main_menu import main_menu
        await message.answer("Добро пожаловать 👇", reply_markup=main_menu)
    else:
        await message.answer("Как тебя зовут?")
        await state.set_state(Reg.name)
