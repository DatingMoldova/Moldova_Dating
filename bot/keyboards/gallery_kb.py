from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def gallery_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить фото", callback_data="add_photo")],
            [InlineKeyboardButton(text="📸 Смотреть фото", callback_data="view_photos")],
            [InlineKeyboardButton(text="⭐ Сделать главным", callback_data="set_main_photo")],
            [InlineKeyboardButton(text="❌ Удалить фото", callback_data="delete_photo")]
        ]
    )
