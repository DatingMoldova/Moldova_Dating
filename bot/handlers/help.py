from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "ℹ️ Помощь")
async def help_cmd(message: Message):
    text = (
        "<blockquote>"
        "ℹ️ ПОМОЩЬ\n\n"

        "👤 Моя анкета — посмотреть или изменить профиль\n"
        "🖼 Галерея — добавить или удалить фото\n"
        "🔍 Смотреть анкеты — поиск людей\n"
        "⭐ Премиум — дополнительные функции\n\n"

        "📄 О нас — информация о сервисе\n"
        "📜 Соглашение — правила использования\n\n"

        "Если что-то не работает — перезапустите бота (/start)"
        "</blockquote>"
    )

    await message.answer(text)
