from aiogram import Router, F
from aiogram.types import Message

from bot.db import get_user

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def my_profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("❌ У вас нет анкеты. Напишите /start")
        return

    text = (
        f"👤 {user[2]}, {user[3]}\n"
        f"📍 {user[4]}\n\n"
        f"{user[5]} → {user[6]}\n\n"
        f"📝 {user[7]}"
    )

    await message.answer_photo(
        photo=user[8],
        caption=text
    )
