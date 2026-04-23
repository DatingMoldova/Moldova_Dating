from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.db import get_user
from bot.keyboards.profile_kb import profile_kb
from bot.keyboards.gallery_kb import gallery_kb
from bot.config import BOT_USERNAME

router = Router()


@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, bot):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Нет анкеты")
        return

    (_, _, name, age, city, gender, search, about,
     photo, _, _, invites, balance,
     _, likes, views, _, is_active) = user

    text = f"""
💖 {name}, {age}
📍 {city}

🚻 {gender}
❤️ {search}

📝 {about}

⭐ {likes*2 + views}
"""

    await bot.send_photo(message.chat.id, photo, caption=text, reply_markup=profile_kb(is_active))


# ===== ГАЛЕРЕЯ =====

@router.callback_query(F.data == "gallery")
async def gallery(call: CallbackQuery):
    await call.message.answer("📸 Галерея", reply_markup=gallery_kb())


# ===== РЕФЕРАЛКА =====

@router.callback_query(F.data == "invite")
async def invite(call: CallbackQuery):
    link = f"https://t.me/{BOT_USERNAME}?start={call.from_user.id}"
    await call.message.answer(f"Твоя ссылка:\n{link}")


# ===== СКРЫТЬ =====

@router.callback_query(F.data == "toggle_profile")
async def toggle(call: CallbackQuery):
    from bot.db import toggle_active
    user = get_user(call.from_user.id)
    new = not user[17]
    toggle_active(call.from_user.id, new)

    await call.message.answer("Статус обновлен")


# ===== ЗАГЛУШКИ =====

@router.message(F.text == "🔥 Смотреть анкеты")
async def search(message: Message):
    await message.answer("Скоро будет 🔥")


@router.message(F.text == "⭐ Премиум")
async def premium(message: Message):
    await message.answer("Премиум скоро 💎")


@router.message(F.text == "🆘 Помощь")
async def help(message: Message):
    await message.answer("Напиши админу")


@router.message(F.text == "ℹ️ О нас")
async def about(message: Message):
    await message.answer("Moldova Dating 🇲🇩")


@router.message(F.text == "📄 Правила")
async def rules(message: Message):
    await message.answer("Правила скоро")
