from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.db import get_user

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    print("START OK")

    user = get_user(message.from_user.id)

    if user:
        from bot.keyboards.main_menu import main_menu
        await message.answer("Добро пожаловать 👇", reply_markup=main_menu)
    else:
        from bot.handlers.register import start_register
        await start_register(message)
