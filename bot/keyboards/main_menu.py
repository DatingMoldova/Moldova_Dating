from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Моя анкета")],
        [KeyboardButton(text="📸 Галерея")],
        [KeyboardButton(text="✏️ Редактировать анкету")],
        [KeyboardButton(text="🔗 Пригласить друга")],
        [KeyboardButton(text="🚫 Скрыть анкету")],
        [KeyboardButton(text="💬 Наш чат")],
        [KeyboardButton(text="🔍 Поиск (в разработке)")]
    ],
    resize_keyboard=True
)
