from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def gallery_main_kb(count: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"➕ Добавить фото ({count}/5)", callback_data="add_photo")],
            [InlineKeyboardButton(text="📸 Мои фото", callback_data="my_photos")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_profile")]
        ]
    )


def photo_actions_kb(photo_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Главное", callback_data=f"set_main_{photo_id}"),
                InlineKeyboardButton(text="❌ Удалить", callback_data=f"del_{photo_id}")
            ]
        ]
    )
