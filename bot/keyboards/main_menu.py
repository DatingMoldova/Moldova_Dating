from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Моя анкета"), KeyboardButton(text="🔥 Смотреть анкеты")],
        [KeyboardButton(text="⭐ Премиум"), KeyboardButton(text="🆘 Помощь")],
        [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="📄 Правила")]
    ],
    resize_keyboard=True
)
