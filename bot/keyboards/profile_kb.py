from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def profile_kb(is_active: bool):
    toggle_text = "🚫 Скрыть анкету" if is_active else "✅ Включить анкету"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Галерея", callback_data="gallery")],
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_profile")],
            [InlineKeyboardButton(text="🔗 Пригласить друга", callback_data="invite")],
            [InlineKeyboardButton(text=toggle_text, callback_data="toggle_profile")]
        ]
    )
