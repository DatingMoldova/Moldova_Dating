from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def agree_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬇️ Свернуть", callback_data="hide_agreement")]
        ]
    )
