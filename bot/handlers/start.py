from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.db import get_user
from bot.config import REQUIRED_CHANNEL, CHANNEL_LINK
from bot.handlers.register import start_register
from bot.keyboards.main_menu import main_menu

router = Router()


# 🔥 ПРОВЕРКА ПОДПИСКИ
async def check_sub(bot, user_id):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🔘 КНОПКА ПОДПИСКИ
def sub_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=CHANNEL_LINK)],
            [InlineKeyboardButton(text="✅ Проверить", callback_data="check_sub")]
        ]
    )


# 🚀 СТАРТ
@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = get_user(message.from_user.id)

    # ❌ НЕ ПОДПИСАН
    if not await check_sub(message.bot, message.from_user.id):
        await message.answer(
            "📢 Для использования бота подпишитесь на канал 👇",
            reply_markup=sub_kb()
        )
        return

    # ✅ ЕСЛИ ЕСТЬ АНКЕТА
    if user:
        await message.answer(
            "Добро пожаловать 👇",
            reply_markup=main_menu()
        )
    else:
        # 🔥 РЕГИСТРАЦИЯ
        await start_register(message, state)


# 🔁 ПРОВЕРКА КНОПКОЙ
@router.callback_query(lambda c: c.data == "check_sub")
async def check_again(call: CallbackQuery, state: FSMContext):

    if await check_sub(call.bot, call.from_user.id):
        user = get_user(call.from_user.id)

        await call.message.edit_text("✅ Подписка подтверждена")

        if user:
            await call.message.answer(
                "Добро пожаловать 👇",
                reply_markup=main_menu()
            )
        else:
            await start_register(call.message, state)

    else:
        await call.answer("❌ Сначала подпишитесь", show_alert=True)
