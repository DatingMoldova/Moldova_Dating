from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.db import get_user, add_view, create_user

router = Router()


class EditProfile(StatesGroup):
    name = State()
    age = State()
    city = State()
    bio = State()
    photo = State()


def profile_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")],
            [InlineKeyboardButton(text="🖼 Галерея", callback_data="gallery")],
            [InlineKeyboardButton(text="👥 Пригласить друга", callback_data="invite")],
            [InlineKeyboardButton(text="❌ Удалить анкету", callback_data="delete")]
        ]
    )


def confirm_delete_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="delete_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="delete_no")
            ]
        ]
    )


# 👤 ПРОФИЛЬ
@router.message(F.text == "👤 Моя анкета")
async def profile(message: Message, state: FSMContext):
    await state.clear()

    user = get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Сначала регистрация")

    add_view(message.from_user.id)

    balance = user[8] or 0
    premium = 1 if user[9] else 0
    invites = user[10] or 0
    views = user[13] or 0
    likes = user[14] or 0
    rep = user[15] or 0

    text = (
        f"👤 <b>{user[1]}, {user[2]}</b>\n\n"
        f"⭐ Репутация: {rep}\n"
        f"❤️ Лайки: {likes}\n"
        f"👀 Просмотры: {views}\n\n"
        f"💰 Баланс: {balance}\n"
        f"👥 Приглашено: {invites}\n"
        f"💎 Премиум: {premium}\n\n"
        f"📍 {user[3]}\n\n"
        f"{user[4]} ищет {user[5]}\n\n"
        f"📝 {user[6]}"
    )

    await message.answer_photo(
        photo=user[7],
        caption=text,
        reply_markup=profile_kb()
    )


# ✏️ РЕДАКТОР
@router.callback_query(F.data == "edit")
async def edit_menu(call: CallbackQuery):
    await call.answer()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="Возраст", callback_data="edit_age")],
        [InlineKeyboardButton(text="Город", callback_data="edit_city")],
        [InlineKeyboardButton(text="О себе", callback_data="edit_bio")],
        [InlineKeyboardButton(text="Фото", callback_data="edit_photo")]
    ])

    await call.message.answer("✏️ Что изменить?", reply_markup=kb)


@router.callback_query(F.data.startswith("edit_"))
async def edit_fields(call: CallbackQuery, state: FSMContext):
    await call.answer()

    field = call.data.split("_")[1]
    await state.set_state(getattr(EditProfile, field))

    await call.message.answer("Введите новое значение")


@router.message(EditProfile.name)
async def edit_name(message: Message, state: FSMContext):
    await update_field(message, state, "name", message.text)


@router.message(EditProfile.age)
async def edit_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Только число")
    await update_field(message, state, "age", int(message.text))


@router.message(EditProfile.city)
async def edit_city(message: Message, state: FSMContext):
    await update_field(message, state, "city", message.text)


@router.message(EditProfile.bio)
async def edit_bio(message: Message, state: FSMContext):
    await update_field(message, state, "bio", message.text)


@router.message(EditProfile.photo, F.photo)
async def edit_photo(message: Message, state: FSMContext):
    await update_field(message, state, "photo", message.photo[-1].file_id)


async def update_field(message, state, field, value):
    user = get_user(message.from_user.id)

    data = {
        "name": user[1],
        "age": user[2],
        "city": user[3],
        "gender": user[4],
        "looking": user[5],
        "bio": user[6],
        "photo": user[7]
    }

    data[field] = value

    create_user(
        message.from_user.id,
        data["name"],
        data["age"],
        data["city"],
        data["gender"],
        data["looking"],
        data["bio"],
        data["photo"]
    )

    await state.clear()
    await message.answer("✅ Обновлено")


# 👥 РЕФЕРАЛКА
@router.callback_query(F.data == "invite")
async def invite(call: CallbackQuery):
    await call.answer()

    bot_username = (await call.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={call.from_user.id}"

    await call.message.answer(f"🔗 {link}")


# ❌ УДАЛЕНИЕ
@router.callback_query(F.data == "delete")
async def delete_profile(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Удалить?", reply_markup=confirm_delete_kb())


@router.callback_query(F.data == "delete_yes")
async def confirm_delete(call: CallbackQuery):
    from bot.db import users

    users.pop(call.from_user.id, None)

    await call.message.answer("❌ Удалено")


@router.callback_query(F.data == "delete_no")
async def cancel_delete(call: CallbackQuery):
    await call.answer()
    await call.message.answer("👌 Отмена")
