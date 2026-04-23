from aiogram import Router, F
from aiogram.types import Message

router = Router()


# 🔍 СМОТРЕТЬ АНКЕТЫ
@router.message(F.text == "🔍 Смотреть анкеты")
async def search(message: Message):
    await message.answer("🔍 Поиск анкет скоро будет")


# ⭐ ПРЕМИУМ
@router.message(F.text == "⭐ Премиум")
async def premium(message: Message):
    await message.answer("⭐ Премиум скоро будет доступен")


# ℹ️ ПОМОЩЬ
@router.message(F.text == "ℹ️ Помощь")
async def help_cmd(message: Message):
    await message.answer("ℹ️ Поддержка скоро появится")


# 📄 О НАС
@router.message(F.text == "📄 О нас")
async def about(message: Message):
    await message.answer("📄 Это дейтинг бот. Найди свою пару ❤️")


# 📜 СОГЛАШЕНИЕ
@router.message(F.text == "📜 Соглашение")
async def agree(message: Message):
    await message.answer("📜 Пользовательское соглашение")
