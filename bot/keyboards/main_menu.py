from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Моя анкета")],
        [KeyboardButton(text="🔍 Поиск")]
    ],
    resize_keyboard=True
)
