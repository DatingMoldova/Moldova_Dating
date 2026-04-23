from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Имя", callback_data="edit_name")],
            [InlineKeyboardButton(text="🎂 Возраст", callback_data="edit_age")],
            [InlineKeyboardButton(text="📍 Город", callback_data="edit_city")],
            [InlineKeyboardButton(text="🚻 Пол", callback_data="edit_gender")],
            [InlineKeyboardButton(text="❤️ Кого ищу", callback_data="edit_search")],
            [InlineKeyboardButton(text="📝 О себе", callback_data="edit_about")]
        ]
    )
