from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscribe_kb(link):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=link)],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ]
    )
