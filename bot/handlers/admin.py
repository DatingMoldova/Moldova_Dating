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
    get_users_count,
    cursor,
    conn
)

router = Router()

ADMIN_ID = int(os.getenv("ADMIN_ID"))


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
            [InlineKeyboardButton(text="🏆 Топ рефералов", callback_data="admin_top")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
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

    await message.answer("🛠 <b>Админ панель</b>", reply_markup=admin_kb())


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
# 🏆 ТОП РЕФЕРАЛОВ
# =========================

@router.callback_query(F.data == "admin_top")
async def top_ref(call: CallbackQuery):
    cursor.execute("""
        SELECT name, invites FROM users
        ORDER BY invites DESC
        LIMIT 10
    """)
    users = cursor.fetchall()

    text = "🏆 <b>Топ по рефералам</b>\n\n"

    for i, u in enumerate(users, start=1):
        text += f"{i}. {u[0]} — {u[1]} 👥\n"

    await call.message.answer(text)


# =========================
# 📊 СТАТИСТИКА
# =========================

@router.callback_query(F.data == "admin_stats")
async def stats(call: CallbackQuery):
    total = get_users_count()

    cursor.execute("SELECT SUM(balance) FROM users")
    total_balance = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(invites) FROM users")
    total_invites = cursor.fetchone()[0] or 0

    text = (
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Пользователей: {total}\n"
        f"👥 Всего рефералов: {total_invites}\n"
        f"💰 Баланс системы: {total_balance}"
    )

    await call.message.answer(text)


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

# =========================
# 📢 РАССЫЛКА
# =========================

@router.callback_query(F.data == "admin_broadcast")
async def broadcast_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📢 Введите текст для рассылки:")
    await state.set_state("broadcast_text")


@router.message(F.text, state="broadcast_text")
async def broadcast_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Отправить", callback_data="broadcast_yes"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="broadcast_no")
            ]
        ]
    )

    await message.answer(
        f"📨 Предпросмотр:\n\n{message.text}",
        reply_markup=kb
    )


@router.callback_query(F.data == "broadcast_yes")
async def broadcast_send(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")

    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    success = 0

    for u in users:
        try:
            await call.bot.send_message(u[0], text)
            success += 1
        except:
            pass

    await call.message.answer(f"✅ Отправлено: {success}")
    await state.clear()


@router.callback_query(F.data == "broadcast_no")
async def broadcast_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("❌ Рассылка отменена")
