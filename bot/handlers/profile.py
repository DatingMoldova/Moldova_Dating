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

    try:
        text = (
            f"👤 {user[1]}, {user[2]}\n"
            f"📍 {user[3]}\n\n"
            f"{user[4]} → {user[5]}\n\n"
            f"📝 {user[6]}"
        )

        await message.answer_photo(
            photo=user[7],
            caption=text
        )

    except Exception as e:
        await message.answer(f"❌ Ошибка профиля: {e}")
