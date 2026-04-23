from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Моя анкета"),
            KeyboardButton(text="🔍 Смотреть анкеты")
        ],
        [
            KeyboardButton(text="⭐ Премиум"),
            KeyboardButton(text="ℹ️ Помощь")
        ],
        [
            KeyboardButton(text="📄 О нас"),
            KeyboardButton(text="📜 Соглашение")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие 👇"
)
