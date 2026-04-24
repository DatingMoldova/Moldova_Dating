from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Моя анкета"),
                KeyboardButton(text="🔍 Смотреть анкеты")
            ],
            [
                KeyboardButton(text="⭐ Премиум"),
                KeyboardButton(text="📩 Поддержка")
            ],
            [
                KeyboardButton(text="🔗 Пригласить друга"),
                KeyboardButton(text="ℹ️ Помощь")
            ],
            [
                KeyboardButton(text="📄 О нас"),
                KeyboardButton(text="📜 Соглашение")
            ]
        ],
        resize_keyboard=True
    )
