from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

gender_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужчина"), KeyboardButton(text="👩 Женщина")],
        [KeyboardButton(text="👫 Пара"), KeyboardButton(text="⚧ Би")]
    ],
    resize_keyboard=True
)

search_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨 Мужчину"), KeyboardButton(text="👩 Девушку")],
        [KeyboardButton(text="👫 Пару"), KeyboardButton(text="⚧ Би")],
        [KeyboardButton(text="🌍 Всех")]
    ],
    resize_keyboard=True
)
