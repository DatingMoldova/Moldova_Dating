from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.agree_kb import agree_kb

router = Router()


# 📜 ПОКАЗ СОГЛАШЕНИЯ
@router.message(F.text == "📜 Соглашение")
async def agreement(message: Message):
    text = (
        "<blockquote>"
        "📜 ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ\n\n"

        "1. ОБЩИЕ ПОЛОЖЕНИЯ\n"
        "Используя бота, вы подтверждаете, что вам 18+.\n\n"

        "2. РЕГИСТРАЦИЯ\n"
        "Запрещено выдавать себя за другого человека.\n\n"

        "3. ЗАПРЕЩЕНО:\n"
        "• спам и реклама\n"
        "• оскорбления\n"
        "• мошенничество\n"
        "• запрещённый контент\n\n"

        "4. КОНТЕНТ\n"
        "Вы несёте ответственность за свои фото и текст.\n\n"

        "5. БЕЗОПАСНОСТЬ\n"
        "Не передавайте личные данные.\n\n"

        "6. ОТВЕТСТВЕННОСТЬ\n"
        "Администрация не отвечает за пользователей.\n\n"

        "7. БЛОКИРОВКА\n"
        "Аккаунт может быть заблокирован без объяснений.\n\n"

        "Используя бота — вы принимаете условия."
        "</blockquote>"
    )

    await message.answer(text, reply_markup=agree_kb())


# ⬇️ СВЕРНУТЬ
@router.callback_query(F.data == "hide_agreement")
async def hide_agreement(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
