from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import get_user, toggle_active, cursor, conn
from bot.keyboards.profile_kb import profile_kb
from bot.keyboards.gallery_kb import gallery_kb
from bot.keyboards.edit_kb import edit_kb
from bot.keyboards.register_kb import gender_kb, search_kb
from bot.config import BOT_USERNAME

router = Router()


# ================= FSM =================

class EditProfile(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()


# ================= ПРОФИЛЬ =================

@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, bot):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Нет анкеты")
        return

    (_, _, name, age, city, gender, search, about,
     photo, _, _, invites, balance,
     _, likes, views, _, is_active) = user

    text = f"""
💖 {name}, {age}
📍 {city}

🚻 {gender}
❤️ {search}

📝 {about}

⭐ Рейтинг: {likes*2 + views}
"""

    await bot.send_photo(
        message.chat.id,
        photo,
        caption=text,
        reply_markup=profile_kb(is_active)
    )


# ================= ГАЛЕРЕЯ =================

@router.callback_query(F.data == "gallery")
async def gallery(call: CallbackQuery):
    await call.message.answer("📸 Галерея", reply_markup=gallery_kb())


# ================= РЕФЕРАЛКА =================

@router.callback_query(F.data == "invite")
async def invite(call: CallbackQuery):
    link = f"https://t.me/{BOT_USERNAME}?start={call.from_user.id}"
    await call.message.answer(f"🔗 Твоя ссылка:\n{link}")


# ================= СКРЫТЬ =================

@router.callback_query(F.data == "toggle_profile")
async def toggle(call: CallbackQuery):
    user = get_user(call.from_user.id)
    new_status = not user[17]

    toggle_active(call.from_user.id, new_status)

    await call.message.answer("✅ Статус анкеты обновлён")


# ================= РЕДАКТИРОВАНИЕ =================

@router.callback_query(F.data == "edit_profile")
async def open_edit(call: CallbackQuery):
    await call.message.answer("Что хочешь изменить?", reply_markup=edit_kb())


# 👤 ИМЯ
@router.callback_query(F.data == "edit_name")
async def edit_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Новое имя:")
    await state.set_state(EditProfile.name)


@router.message(EditProfile.name)
async def save_name(message: Message, state: FSMContext):
    cursor.execute(
        "UPDATE users SET name = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Имя обновлено")
    await state.clear()


# 🎂 ВОЗРАСТ
@router.callback_query(F.data == "edit_age")
async def edit_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Новый возраст (16+):")
    await state.set_state(EditProfile.age)


@router.message(EditProfile.age)
async def save_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16:
        await message.answer("Только 16+")
        return

    cursor.execute(
        "UPDATE users SET age = %s WHERE user_id = %s",
        (int(message.text), message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Возраст обновлён")
    await state.clear()


# 📍 ГОРОД
@router.callback_query(F.data == "edit_city")
async def edit_city(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Новый город:")
    await state.set_state(EditProfile.city)


@router.message(EditProfile.city)
async def save_city(message: Message, state: FSMContext):
    cursor.execute(
        "UPDATE users SET city = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Город обновлён")
    await state.clear()


# 🚻 ПОЛ
@router.callback_query(F.data == "edit_gender")
async def edit_gender(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Выбери пол 👇", reply_markup=gender_kb)
    await state.set_state(EditProfile.gender)


@router.message(EditProfile.gender)
async def save_gender(message: Message, state: FSMContext):
    if message.text not in ["👨 Мужчина", "👩 Женщина", "👫 Пара", "⚧ Би"]:
        await message.answer("Выбери кнопку")
        return

    cursor.execute(
        "UPDATE users SET gender = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Пол обновлён")
    await state.clear()


# ❤️ КОГО ИЩУ
@router.callback_query(F.data == "edit_search")
async def edit_search(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Кого ищешь 👇", reply_markup=search_kb)
    await state.set_state(EditProfile.search)


@router.message(EditProfile.search)
async def save_search(message: Message, state: FSMContext):
    if message.text not in ["👨 Мужчину", "👩 Девушку", "👫 Пару", "⚧ Би", "🌍 Всех"]:
        await message.answer("Выбери кнопку")
        return

    cursor.execute(
        "UPDATE users SET search = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Обновлено")
    await state.clear()


# 📝 О СЕБЕ
@router.callback_query(F.data == "edit_about")
async def edit_about(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Новый текст:")
    await state.set_state(EditProfile.about)


@router.message(EditProfile.about)
async def save_about(message: Message, state: FSMContext):
    cursor.execute(
        "UPDATE users SET about = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("✅ Описание обновлено")
    await state.clear()


# ================= ЗАГЛУШКИ =================

@router.message(F.text == "🔥 Смотреть анкеты")
async def search(message: Message):
    await message.answer("🔥 Скоро будет")


@router.message(F.text == "⭐ Премиум")
async def premium(message: Message):
    await message.answer("💎 Скоро будет")


@router.message(F.text == "🆘 Помощь")
async def help(message: Message):
    await message.answer("Напиши админу")


@router.message(F.text == "ℹ️ О нас")
async def about(message: Message):
    await message.answer("Moldova Dating 🇲🇩")


@router.message(F.text == "📄 Правила")
async def rules(message: Message):
    await message.answer("📄 Правила внутри кнопки")
