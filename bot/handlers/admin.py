import os

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.db import (
    set_premium,
    create_promo,
    add_moderator,
    cursor,
    conn
)

router = Router()

ADMIN_ID = int(os.getenv("ADMIN_ID"))


# 🔒 ПРОВЕРКА
def is_admin(user_id):
    return user_id == ADMIN_ID


# =========================
# 🔘 КНОПКИ
# =========================

def admin_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Премиум", callback_data="admin_premium")],
            [InlineKeyboardButton(text="🎁 Промокод", callback_data="admin_promo")],
            [InlineKeyboardButton(text="🛡 Модератор", callback_data="admin_mod")],
            [InlineKeyboardButton(text="💣 Сброс БД", callback_data="admin_reset")]
        ]
    )


# =========================
# 🛠 ПАНЕЛЬ
# =========================

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🛠 <b>Админ панель</b>",
        reply_markup=admin_kb()
    )


# =========================
# ⭐ ПРЕМИУМ
# =========================

@router.callback_query(F.data == "admin_premium")
async def premium_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ID пользователя:")
    await state.set_state("premium_user")


@router.message(F.text, state="premium_user")
async def premium_user(message: Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    await message.answer("Включить премиум? (да/нет)")
    await state.set_state("premium_confirm")


@router.message(F.text, state="premium_confirm")
async def premium_confirm(message: Message, state: FSMContext):
    data = await state.get_data()

    status = message.text.lower() == "да"

    set_premium(data["user_id"], status)

    await message.answer("✅ Премиум обновлён")
    await state.clear()


# =========================
# 🎁 ПРОМО
# =========================

@router.callback_query(F.data == "admin_promo")
async def promo_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите код промо:")
    await state.set_state("promo_code")


@router.message(F.text, state="promo_code")
async def promo_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Введите награду:")
    await state.set_state("promo_reward")


@router.message(F.text, state="promo_reward")
async def promo_reward(message: Message, state: FSMContext):
    data = await state.get_data()

    create_promo(data["code"], int(message.text))

    await message.answer("🎁 Промокод создан")
    await state.clear()


# =========================
# 🛡 МОДЕРАТОР
# =========================

@router.callback_query(F.data == "admin_mod")
async def mod_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ID пользователя:")
    await state.set_state("mod_user")


@router.message(F.text, state="mod_user")
async def mod_add(message: Message, state: FSMContext):
    add_moderator(int(message.text))

    await message.answer("🛡 Модератор назначен")
    await state.clear()


# =========================
# 💣 СБРОС БД
# =========================

def confirm_reset_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="reset_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="reset_no")
            ]
        ]
    )


@router.callback_query(F.data == "admin_reset")
async def reset_confirm(call: CallbackQuery):
    await call.message.answer(
        "⚠️ Удалить ВСЮ базу?",
        reply_markup=confirm_reset_kb()
    )


@router.callback_query(F.data == "reset_yes")
async def reset_db(call: CallbackQuery):
    cursor.execute("TRUNCATE users, promos, moderators RESTART IDENTITY CASCADE")
    conn.commit()

    await call.message.answer("💣 База полностью очищена")


@router.callback_query(F.data == "reset_no")
async def cancel_reset(call: CallbackQuery):
    await call.message.answer("👌 Отмена")
