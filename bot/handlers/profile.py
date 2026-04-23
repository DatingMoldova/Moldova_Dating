from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.db import get_user, toggle_active, reset_db
from bot.keyboards.profile_kb import profile_kb

router = Router()


# 👤 МОЯ АНКЕТА
@router.message(F.text == "👤 Моя анкета")
async def my_profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("❌ У вас нет анкеты. Напишите /start")
        return

    text = (
        f"👤 {user[2]}, {user[3]}\n"
        f"📍 {user[4]}\n\n"
        f"{user[5]} → {user[6]}\n\n"
        f"📝 {user[7]}"
    )

    await message.answer_photo(
        photo=user[8],
        caption=text,
        reply_markup=profile_kb(user[16])  # is_active
    )


# 🙈 СКРЫТЬ / ВКЛ
@router.callback_query(F.data == "toggle_profile")
async def toggle_profile_handler(call: CallbackQuery):
    user = get_user(call.from_user.id)

    new_status = not user[16]

    toggle_active(call.from_user.id, new_status)

    await call.answer("Обновлено")

    await call.message.edit_reply_markup(
        reply_markup=profile_kb(new_status)
    )


# 🗑 УДАЛИТЬ
@router.callback_query(F.data == "delete_profile")
async def delete_profile(call: CallbackQuery):
    from bot.db import cursor, conn

    cursor.execute("DELETE FROM users WHERE user_id = %s", (call.from_user.id,))
    conn.commit()

    await call.answer()
    await call.message.delete()

    await call.message.answer("🗑 Анкета удалена. Напишите /start")
