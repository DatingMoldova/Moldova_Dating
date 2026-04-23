from aiogram import Router, F
from aiogram.types import Message

from bot.db import get_user
from bot.config import BOT_USERNAME

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, bot):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Нет анкеты")
        return

    (_, user_id, name, age, city, gender, search, about,
     photo, username, referrer_id, invites, balance, _) = user

    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    text = (
        f"💖 Твоя анкета\n\n"
        f"👤 {name}, {age}\n"
        f"📍 {city}\n"
        f"🚻 {gender} | ❤️ Ищешь: {search}\n\n"
        f"📝 {about}\n\n"
        f"👥 Приглашено: {invites}\n"
        f"💰 Баланс: {balance}\n\n"
        f"🔗 <a href='{ref_link}'>Пригласить друга</a>"
    )

    await bot.send_photo(
        message.chat.id,
        photo=photo,
        caption=text,
        parse_mode="HTML"
    )


@router.message(F.text == "💬 Наш чат")
async def chat(message: Message):
    await message.answer("https://t.me/your_chat")


@router.message(F.text == "🔍 Поиск (в разработке)")
async def search(message: Message):
    await message.answer("В разработке 🔧")
