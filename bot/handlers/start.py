from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

from bot.config import REQUIRED_CHANNEL, CHANNEL_LINK
from bot.db import get_user

router = Router()


async def check_sub(message: Message):
    try:
        member = await message.bot.get_chat_member(REQUIRED_CHANNEL, message.from_user.id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@router.message(Command("start"))
async def start(message: Message):
    print("START WORKING")

    user = get_user(message.from_user.id)

    if not await check_sub(message):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=CHANNEL_LINK)],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ])
        await message.answer("Подпишись на канал 👇", reply_markup=kb)
        return

    if user:
        from bot.keyboards.main_menu import main_menu
        await message.answer("Добро пожаловать 👇", reply_markup=main_menu)
    else:
        from bot.handlers.register import start_register
        await start_register(message)


@router.callback_query(lambda c: c.data == "check_sub")
async def check_again(call: CallbackQuery):
    try:
        member = await call.bot.get_chat_member(REQUIRED_CHANNEL, call.from_user.id)
        ok = member.status in ["member", "administrator", "creator"]
    except:
        ok = False

    if ok:
        from bot.handlers.register import start_register
        await call.message.answer("✅ Подписка есть, начинаем регистрацию")
        await start_register(call.message)
    else:
        await call.answer("❌ Подпишись сначала", show_alert=True)
