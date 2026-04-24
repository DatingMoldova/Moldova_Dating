from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "📄 О нас")
async def about(message: Message):
    text = (
        "<blockquote>"
        "📄 О НАС\n\n"

        "Это современный бот для знакомств ❤️\n\n"

        "Здесь ты можешь:\n"
        "• находить интересных людей\n"
        "• общаться\n"
        "• создавать знакомства\n\n"

        "Мы делаем сервис простым и удобным.\n\n"

        "Спасибо, что ты с нами 🚀"
        "</blockquote>"
    )

    await message.answer(text)
