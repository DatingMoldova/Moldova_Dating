from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import (
    get_user,
    update_user_field,
    delete_user,
    add_photo,
    get_photos,
    delete_photo,
    set_main_photo
)

from bot.keyboards.profile_kb import profile_kb, edit_kb, confirm_delete_kb
from bot.keyboards.gallery_kb import gallery_main_kb, photo_actions_kb

router = Router()


# =========================
# STATES
# =========================

class Edit(StatesGroup):
    name = State()
    age = State()
    city = State()
    about = State()


class GalleryState(StatesGroup):
    add = State()


# =========================
# 👤 ПРОФИЛЬ
# =========================

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
        reply_markup=profile_kb()
    )


# =========================
# 🗑 УДАЛЕНИЕ (С ПОДТВЕРЖДЕНИЕМ)
# =========================

@router.callback_query(F.data == "delete_profile")
async def delete_profile_start(call: CallbackQuery):
    await call.answer()

    await call.message.answer(
        "❗ Вы точно хотите удалить анкету?",
        reply_markup=confirm_delete_kb()
    )


@router.callback_query(F.data == "confirm_delete")
async def confirm_delete(call: CallbackQuery):
    await call.answer()

    delete_user(call.from_user.id)

    await call.message.delete()
    await call.message.answer("🗑 Анкета удалена. Напишите /start")


@router.callback_query(F.data == "cancel_delete")
async def cancel_delete(call: CallbackQuery):
    await call.answer("Отмена")
    await call.message.delete()


# =========================
# ✏️ РЕДАКТОР
# =========================

@router.callback_query(F.data == "edit_profile")
async def open_editor(call: CallbackQuery):
    await call.answer()
    await call.message.answer("✏️ Что изменить?", reply_markup=edit_kb())


# 👤 имя
@router.callback_query(F.data == "edit_name")
async def edit_name_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Введите новое имя:")
    await state.set_state(Edit.name)


@router.message(Edit.name)
async def edit_name_save(message: Message, state: FSMContext):
    update_user_field(message.from_user.id, "name", message.text)
    await message.answer("✅ Имя обновлено")
    await state.clear()


# 🎂 возраст
@router.callback_query(F.data == "edit_age")
async def edit_age_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Введите возраст:")
    await state.set_state(Edit.age)


@router.message(Edit.age)
async def edit_age_save(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите число")
        return

    update_user_field(message.from_user.id, "age", int(message.text))
    await message.answer("✅ Возраст обновлен")
    await state.clear()


# 📍 город
@router.callback_query(F.data == "edit_city")
async def edit_city_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Введите город:")
    await state.set_state(Edit.city)


@router.message(Edit.city)
async def edit_city_save(message: Message, state: FSMContext):
    update_user_field(message.from_user.id, "city", message.text)
    await message.answer("✅ Город обновлен")
    await state.clear()


# 📝 о себе
@router.callback_query(F.data == "edit_about")
async def edit_about_start(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Напишите о себе:")
    await state.set_state(Edit.about)


@router.message(Edit.about)
async def edit_about_save(message: Message, state: FSMContext):
    update_user_field(message.from_user.id, "about", message.text)
    await message.answer("✅ Описание обновлено")
    await state.clear()


# =========================
# 🖼 ГАЛЕРЕЯ
# =========================

@router.callback_query(F.data == "gallery")
async def open_gallery(call: CallbackQuery):
    await call.answer()

    photos = get_photos(call.from_user.id)
    count = len(photos)

    await call.message.answer(
        f"🖼 Галерея\n\nФото: {count}/5",
        reply_markup=gallery_main_kb(count)
    )


# ➕ добавить фото
@router.callback_query(F.data == "add_photo")
async def add_photo_start(call: CallbackQuery, state: FSMContext):
    await call.answer()

    photos = get_photos(call.from_user.id)

    if len(photos) >= 5:
        await call.message.answer("❌ Уже 5 фото")
        return

    await call.message.answer("📸 Отправьте фото")
    await state.set_state(GalleryState.add)


@router.message(GalleryState.add, F.photo)
async def save_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id

    ok = add_photo(message.from_user.id, file_id)

    if not ok:
        await message.answer("❌ Лимит 5 фото")
    else:
        await message.answer("✅ Фото добавлено")

    await state.clear()


# 📸 мои фото
@router.callback_query(F.data == "my_photos")
async def my_photos(call: CallbackQuery):
    await call.answer()

    photos = get_photos(call.from_user.id)

    if not photos:
        await call.message.answer("❌ Нет фото")
        return

    for i, (photo_id, file_id) in enumerate(photos, start=1):
        await call.message.answer_photo(
            photo=file_id,
            caption=f"Фото {i}",
            reply_markup=photo_actions_kb(photo_id)
        )


# ⭐ главное фото
@router.callback_query(F.data.startswith("set_main_"))
async def set_main(call: CallbackQuery):
    await call.answer()

    photo_id = int(call.data.split("_")[2])
    photos = get_photos(call.from_user.id)

    for pid, file_id in photos:
        if pid == photo_id:
            set_main_photo(call.from_user.id, file_id)
            await call.message.answer("⭐ Главное фото обновлено")
            return


# ❌ удалить фото
@router.callback_query(F.data.startswith("del_"))
async def delete_photo_handler(call: CallbackQuery):
    await call.answer()

    photo_id = int(call.data.split("_")[1])

    delete_photo(photo_id)

    await call.message.delete()
    await call.message.answer("❌ Фото удалено")


# =========================
# ⬅️ НАЗАД
# =========================

@router.callback_query(F.data == "back_profile")
async def back_profile(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
