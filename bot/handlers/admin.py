from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import ADMIN_ID
from bot.db import reset_db

router = Router()


def is_admin(user_id: int):
    return user_id == ADMIN_ID


# 🔐 админ-панель
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ Админ-панель:\n\n"
        "/reset - очистить БД\n"
        "/users - количество пользователей\n"
        "/test - проверка"
    )


# 💣 сброс БД
@router.message(Command("reset"))
async def reset(message: Message):
    if not is_admin(message.from_user.id):
        return

    reset_db()
    await message.answer("💥 База данных очищена")


# 📊 пользователи
@router.message(Command("users"))
async def users(message: Message):
    if not is_admin(message.from_user.id):
        return

    from bot.db import cursor
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    await message.answer(f"👥 Пользователей: {count}")


# 🧪 тест
@router.message(Command("test"))
async def test(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer("✅ Админка работает")
