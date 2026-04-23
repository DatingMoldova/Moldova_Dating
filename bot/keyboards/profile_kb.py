from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile"),
                InlineKeyboardButton(text="🖼 Галерея", callback_data="gallery")
            ],
            [
                InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_profile")
            ]
        ]
    )


def edit_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Имя", callback_data="edit_name")],
            [InlineKeyboardButton(text="🎂 Возраст", callback_data="edit_age")],
            [InlineKeyboardButton(text="📍 Город", callback_data="edit_city")],
            [InlineKeyboardButton(text="📝 О себе", callback_data="edit_about")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_profile")]
        ]
    )


def confirm_delete_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_delete"),
                InlineKeyboardButton(text="❌ Нет", callback_data="cancel_delete")
            ]
        ]
    )
