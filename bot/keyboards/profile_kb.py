from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_kb(is_active: bool):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile"),
                InlineKeyboardButton(text="🖼 Галерея", callback_data="gallery")
            ],
            [
                InlineKeyboardButton(
                    text="🙈 Скрыть" if is_active else "👁 Включить",
                    callback_data="toggle_profile"
                )
            ],
            [
                InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_profile")
            ]
        ]
    )
