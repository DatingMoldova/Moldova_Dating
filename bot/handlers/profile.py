from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import get_user, toggle_active, update_user_field
from bot.keyboards.profile_kb import profile_kb, edit_kb

router = Router()


class Edit(StatesGroup):
    name = State()
    age = State()
    city = State()
    about = State()


# 👤 МОЯ АНКЕТА
@router.message(F.text == "👤 Моя анкета")
async def my_profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        await message.answer("❌ Нет анкеты. /start")
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
        reply_markup=profile_kb(user[16])
    )


# ✏️ ОТКРЫТЬ РЕДАКТОР
@router.callback_query(F.data == "edit_profile")
async def open_editor(call: CallbackQuery):
    await call.answer()

    await call.message.answer(
        "✏️ Что хотите изменить?",
        reply_markup=edit_kb()
    )


# 👤 ИМЯ
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


# 🎂 ВОЗРАСТ
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


# 📍 ГОРОД
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


# 📝 О СЕБЕ
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


# ⬅️ НАЗАД
@router.callback_query(F.data == "back_profile")
async def back_profile(call: CallbackQuery):
    await call.answer()
    await call.message.delete()
