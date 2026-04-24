from aiogram import Router, F
from aiogram.types import Message

from bot.db import get_incoming_likes, get_outgoing_likes, get_user

router = Router()


@router.message(F.text == "❤️ Мои симпатии")
async def my_likes(message: Message):
    user_id = message.from_user.id

    incoming = get_incoming_likes(user_id)
    outgoing = get_outgoing_likes(user_id)

    text = "❤️ <b>Мои симпатии</b>\n\n"

    # 💘 кто лайкнул
    text += "💌 <b>Тебя лайкнули:</b>\n"
    if incoming:
        for u in incoming[:5]:
            user = get_user(u[0])
            if user:
                text += f"• {user[2]}, {user[3]}\n"
    else:
        text += "— пока нет\n"

    text += "\n"

    # 👉 кого ты лайкнул
    text += "👉 <b>Ты лайкнул:</b>\n"
    if outgoing:
        for u in outgoing[:5]:
            user = get_user(u[0])
            if user:
                text += f"• {user[2]}, {user[3]}\n"
    else:
        text += "— пока нет\n"

    text += "\n💡 Взаимные лайки = 💘 матч"

    await message.answer(text)
