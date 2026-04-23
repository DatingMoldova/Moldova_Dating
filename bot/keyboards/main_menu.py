from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Моя анкета")],
        [KeyboardButton(text="💬 Наш чат")],
        [KeyboardButton(text="🔍 Поиск (в разработке)")]
    ],
    resize_keyboard=True
)
