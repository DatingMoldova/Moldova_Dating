from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

from bot.config import REQUIRED_CHANNEL, CHANNEL_LINK
from bot.db import get_user

router = Router()


async def check_sub(bot, user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@router.message(Command("start"))
async def start(message: Message, bot):
    print("START OK")

    user = get_user(message.from_user.id)

    if not await check_sub(bot, message.from_user.id):
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
async def check_again(call: CallbackQuery, bot):
    if await check_sub(bot, call.from_user.id):
        from bot.handlers.register import start_register
        await call.message.answer("✅ Подписка есть, начинаем регистрацию")
        await start_register(call.message)
    else:
        await call.answer("❌ Подпишись сначала", show_alert=True)
