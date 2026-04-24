from aiogram import Bot

from bot.config import LOG_CHAT_ID, LOG_THREAD_ID


async def log_profile(bot: Bot, user):
    text = (
        "📥 <b>Новая анкета</b>\n\n"

        f"👤 {user[2]}, {user[3]}\n"
        f"📍 {user[4]}\n\n"
        f"{user[5]} → {user[6]}\n\n"
        f"📝 {user[7]}\n\n"

        f"🆔 {user[1]}"
    )

    try:
        await bot.send_photo(
            chat_id=LOG_CHAT_ID,
            message_thread_id=LOG_THREAD_ID,
            photo=user[8],
            caption=text
        )
    except Exception as e:
        print("LOG ERROR:", e)
