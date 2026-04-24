from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import ADMIN_ID

router = Router()


@router.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("Админка работает")
