from aiogram import Router, F
from aiogram.types import Message

router = Router()


# 🔍 СМОТРЕТЬ АНКЕТЫ
@router.message(F.text == "🔍 Смотреть анкеты")
async def search(message: Message):
    await message.answer("🔍 Поиск анкет скоро будет")
