from aiogram import Router, F
from aiogram.types import Message

from bot.db import get_user
from bot.handlers.register import start_register

router = Router()


# =========================
# 🚀 СТАРТ
# =========================

@router.message(F.text == "/start")
async def start(message: Message):
    user = get_user(message.from_user.id)

    if user:
        from bot.keyboards.main_menu import main_menu
        await message.answer("👋 С возвращением!", reply_markup=main_menu())
    else:
        await start_register(message, state=None)


# =========================
# 👤 ПРОФИЛЬ
# =========================

@router.message(F.text == "👤 Моя анкета")
async def my_profile(message: Message):
    # просто триггер, логика уже в profile.py
    pass


# =========================
# 🔍 СМОТРЕТЬ АНКЕТЫ
# =========================

@router.message(F.text == "🔍 Смотреть анкеты")
async def browse(message: Message):
    await message.answer("🔍 Поиск анкет скоро будет доступен")


# =========================
# ⭐ ПРЕМИУМ
# =========================

@router.message(F.text == "⭐ Премиум")
async def premium(message: Message):
    await message.answer("⭐ Премиум скоро будет доступен")


# =========================
# ❤️ ЛАЙКИ
# =========================

@router.message(F.text == "❤️ Мои симпатии")
async def likes(message: Message):
    await message.answer("❤️ Здесь будут лайки")


# =========================
# 📩 ПОДДЕРЖКА
# =========================

@router.message(F.text == "📩 Поддержка")
async def support(message: Message):
    await message.answer("📩 Напишите администратору")


# =========================
# ℹ️ ПОМОЩЬ
# =========================

@router.message(F.text == "ℹ️ Помощь")
async def help_cmd(message: Message):
    await message.answer("ℹ️ Помощь скоро будет")


# =========================
# 📄 О НАС
# =========================

@router.message(F.text == "📄 О нас")
async def about(message: Message):
    await message.answer("📄 О проекте")


# =========================
# 📜 СОГЛАШЕНИЕ
# =========================

@router.message(F.text == "📜 Соглашение")
async def rules(message: Message):
    await message.answer("📜 Пользовательское соглашение")
