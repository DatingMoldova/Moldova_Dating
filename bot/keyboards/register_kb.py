from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )


def gender_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨 Мужчина", callback_data="g_male")],
            [InlineKeyboardButton(text="👩 Женщина", callback_data="g_female")],
            [InlineKeyboardButton(text="👫 Пара", callback_data="g_pair")],
            [InlineKeyboardButton(text="⚧ Би", callback_data="g_bi")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )


def search_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨 Мужчину", callback_data="s_male")],
            [InlineKeyboardButton(text="👩 Девушку", callback_data="s_female")],
            [InlineKeyboardButton(text="👫 Пару", callback_data="s_pair")],
            [InlineKeyboardButton(text="⚧ Би", callback_data="s_bi")],
            [InlineKeyboardButton(text="🌍 Всех", callback_data="s_all")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )
