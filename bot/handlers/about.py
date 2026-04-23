from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📄 О нас")
async def about(message: Message):
    text = (
        "<blockquote>"
        "📄 О НАС\n\n"

        "Это современный дейтинг-бот для знакомств.\n\n"

        "💬 Общайтесь\n"
        "❤️ Находите симпатии\n"
        "🔥 Встречайтесь\n\n"

        "Мы создали простой и удобный сервис,\n"
        "чтобы вы могли находить интересных людей рядом.\n\n"

        "🚀 Бот постоянно развивается\n"
        "и получает новые функции.\n\n"

        "Спасибо, что вы с нами ❤️"
        "</blockquote>"
    )

    await message.answer(text)
