from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import get_user
from bot.config import BOT_USERNAME
from bot.keyboards.gallery_kb import gallery_kb

router = Router()


# ================= FSM =================

class PhotoEdit(StatesGroup):
    add = State()
    delete = State()
    set_main = State()


class EditProfile(StatesGroup):
    about = State()


# ================= ПРОФИЛЬ =================

@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, bot):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("Нет анкеты")
        return

    (_, user_id, name, age, city, gender, search, about,
     photo, username, referrer_id, invites, balance,
     is_counted, likes, views, photos, is_active) = user

    rating = likes * 2 + views

    text = (
        f"💖 <b>{name}, {age}</b>\n"
        f"📍 {city}\n\n"
        f"🚻 {gender}\n"
        f"❤️ {search}\n\n"
        f"📝 {about}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"⭐ Рейтинг: {rating}\n"
        f"❤️ {likes} | 👁 {views}\n\n"
        f"👥 {invites} | 💰 {balance}"
    )

    await bot.send_photo(
        message.chat.id,
        photo=photo,
        caption=text,
        parse_mode="HTML"
    )


# ================= ГАЛЕРЕЯ =================

@router.message(F.text == "📸 Галерея")
async def gallery(message: Message):
    await message.answer("Управление фото 👇", reply_markup=gallery_kb())


# ➕ ДОБАВИТЬ

@router.callback_query(F.data == "add_photo")
async def add_photo(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отправь фото (макс 5)")
    await state.set_state(PhotoEdit.add)


@router.message(PhotoEdit.add, F.photo)
async def save_photo(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    photos = user[14] or []

    if len(photos) >= 5:
        await message.answer("Максимум 5 фото")
        return

    photo_id = message.photo[-1].file_id
    photos.append(photo_id)

    from bot.db import cursor, conn
    cursor.execute(
        "UPDATE users SET photos = %s WHERE user_id = %s",
        (photos, message.from_user.id)
    )
    conn.commit()

    await message.answer(f"✅ Добавлено ({len(photos)}/5)")


# 👀 СМОТРЕТЬ

@router.callback_query(F.data == "view_photos")
async def view_photos(call: CallbackQuery, bot):
    user = get_user(call.from_user.id)
    photos = user[14]

    if not photos:
        await call.answer("Нет фото", show_alert=True)
        return

    for p in photos:
        await bot.send_photo(call.message.chat.id, p)


# ❌ УДАЛИТЬ

@router.callback_query(F.data == "delete_photo")
async def delete_photo(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Номер фото для удаления (1-5)")
    await state.set_state(PhotoEdit.delete)


@router.message(PhotoEdit.delete)
async def delete_process(message: Message, state: FSMContext):
    index = int(message.text) - 1

    user = get_user(message.from_user.id)
    photos = user[14] or []

    if index >= len(photos):
        await message.answer("Нет такого фото")
        return

    photos.pop(index)

    from bot.db import cursor, conn
    cursor.execute(
        "UPDATE users SET photos = %s WHERE user_id = %s",
        (photos, message.from_user.id)
    )
    conn.commit()

    await message.answer("Удалено")
    await state.clear()


# ⭐ ГЛАВНОЕ

@router.callback_query(F.data == "set_main_photo")
async def set_main(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Номер фото сделать главным")
    await state.set_state(PhotoEdit.set_main)


@router.message(PhotoEdit.set_main)
async def set_main_process(message: Message, state: FSMContext):
    index = int(message.text) - 1

    user = get_user(message.from_user.id)
    photos = user[14] or []

    if index >= len(photos):
        await message.answer("Нет такого фото")
        return

    main_photo = photos[index]

    from bot.db import cursor, conn
    cursor.execute(
        "UPDATE users SET photo = %s WHERE user_id = %s",
        (main_photo, message.from_user.id)
    )
    conn.commit()

    await message.answer("Главное фото обновлено")
    await state.clear()


# ================= РЕДАКТИРОВАНИЕ =================

@router.message(F.text == "✏️ Редактировать анкету")
async def edit_profile(message: Message, state: FSMContext):
    await message.answer("Напиши новый текст о себе")
    await state.set_state(EditProfile.about)


@router.message(EditProfile.about)
async def update_about(message: Message, state: FSMContext):
    from bot.db import cursor, conn

    cursor.execute(
        "UPDATE users SET about = %s WHERE user_id = %s",
        (message.text, message.from_user.id)
    )
    conn.commit()

    await message.answer("Анкета обновлена")
    await state.clear()


# ================= СКРЫТЬ =================

@router.message(F.text == "🚫 Скрыть анкету")
async def toggle_profile(message: Message):
    user = get_user(message.from_user.id)
    is_active = user[15]

    from bot.db import cursor, conn

    new_status = not is_active

    cursor.execute(
        "UPDATE users SET is_active = %s WHERE user_id = %s",
        (new_status, message.from_user.id)
    )
    conn.commit()

    if new_status:
        await message.answer("Анкета включена")
    else:
        await message.answer("Анкета скрыта")
