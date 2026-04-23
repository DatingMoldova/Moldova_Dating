from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "⭐ Премиум")
async def premium(message: Message):
    text = (
        "<blockquote>"
        "⭐ ПРЕМИУМ\n\n"

        "Открой больше возможностей:\n\n"

        "🔥 Поднятие анкеты в топ\n"
        "❤️ Безлимитные лайки\n"
        "👀 Смотреть, кто лайкнул вас\n"
        "🚫 Без рекламы\n"
        "⚡ Быстрые совпадения\n\n"

        "Скоро будет доступно 🚀"
        "</blockquote>"
    )

    await message.answer(text)
