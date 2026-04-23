from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscribe_kb(channel_link):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=channel_link)],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ]
    )
