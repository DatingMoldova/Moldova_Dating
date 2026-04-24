from aiogram import Router, F
from aiogram.types import Message

from bot.db import get_user

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        return await message.answer("Нет анкеты")

    await message.answer_photo(
        photo=user[7],
        caption=f"{user[1]}, {user[2]}"
    )
