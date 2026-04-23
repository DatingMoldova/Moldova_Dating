from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.db import get_user
from bot.config import REQUIRED_CHANNEL, CHANNEL_LINK
from bot.handlers.register import start_reg

router = Router()


# 🔥 проверка подписки
async def check_sub(bot, user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🚀 СТАРТ
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    print("START OK")

    user = get_user(message.from_user.id)

    # 📢 проверка подписки
    if not await check_sub(message.bot, message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=CHANNEL_LINK)],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ])
        await message.answer("Подпишитесь на канал 👇", reply_markup=kb)
        return

    # 👤 если уже есть анкета
    if user:
        from bot.keyboards.main_menu import main_menu
        await message.answer("Добро пожаловать 👇", reply_markup=main_menu)
    else:
        # 🔥 новая регистрация (без мусора)
        await start_reg(message, state)


# 🔁 проверка подписки кнопкой
@router.callback_query(lambda c: c.data == "check_sub")
async def check_again(call: CallbackQuery, state: FSMContext):
    if await check_sub(call.bot, call.from_user.id):
        await call.message.answer("✅ Подписка подтверждена")
        await start_reg(call.message, state)
    else:
        await call.answer("❌ Сначала подпишитесь", show_alert=True)
