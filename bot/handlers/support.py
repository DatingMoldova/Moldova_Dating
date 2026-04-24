from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import os

router = Router()

SUPPORT_CHAT_ID = int(os.getenv("SUPPORT_CHAT_ID"))
SUPPORT_TOPIC_ID = int(os.getenv("SUPPORT_TOPIC_ID"))


# =========================
# 🔥 СТЕЙТЫ
# =========================

class SupportState(StatesGroup):
    waiting_text = State()
    reply_text = State()


# =========================
# 🎫 СОЗДАНИЕ ТИКЕТА
# =========================

@router.message(F.text == "📩 Поддержка")
async def support_start(message: Message, state: FSMContext):
    await message.answer("✍️ Напишите ваше сообщение:")
    await state.set_state(SupportState.waiting_text)


@router.message(SupportState.waiting_text)
async def send_ticket(message: Message, state: FSMContext):
    user = message.from_user

    text = (
        f"📩 <b>Новый тикет</b>\n\n"
        f"👤 {user.full_name}\n"
        f"🆔 {user.id}\n"
        f"@{user.username}\n\n"
        f"💬 {message.text}"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Ответить", callback_data=f"reply_{user.id}"),
                InlineKeyboardButton(text="🔒 Закрыть", callback_data="close_ticket")
            ]
        ]
    )

    await message.bot.send_message(
        chat_id=SUPPORT_CHAT_ID,
        message_thread_id=SUPPORT_TOPIC_ID,
        text=text,
        reply_markup=kb
    )

    await message.answer("✅ Тикет отправлен")
    await state.clear()


# =========================
# 💬 ОТВЕТ
# =========================

@router.callback_query(F.data.startswith("reply_"))
async def reply_ticket(call: CallbackQuery, state: FSMContext):
    user_id = int(call.data.split("_")[1])

    await state.update_data(reply_user=user_id)
    await call.message.answer("✍️ Введите ответ:")
    await state.set_state(SupportState.reply_text)


@router.message(SupportState.reply_text)
async def send_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("reply_user")

    await message.bot.send_message(
        user_id,
        f"💬 Ответ поддержки:\n\n{message.text}"
    )

    await message.answer("✅ Ответ отправлен")
    await state.clear()


# =========================
# 🔒 ЗАКРЫТЬ
# =========================

@router.callback_query(F.data == "close_ticket")
async def close_ticket(call: CallbackQuery):
    await call.message.edit_text(call.message.text + "\n\n🔒 Тикет закрыт")
