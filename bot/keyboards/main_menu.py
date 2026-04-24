from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Моя анкета"),
                KeyboardButton(text="🔍 Смотреть анкеты")
            ]
        ],
        resize_keyboard=True
    )
