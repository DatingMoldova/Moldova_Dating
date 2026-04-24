from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.db import get_user, add_view, create_user

router = Router()


# 🔥 СТЕЙТЫ РЕДАКТОРА
class EditProfile(StatesGroup):
    name = State()
    age = State()
    city = State()
    about = State()
    photo = State()


# 🔘 КНОПКИ
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
async def profile(message: Message):
    user = get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Сначала регистрация")

    add_view(message.from_user.id)

    text = (
        f"👤 <b>{user[2]}, {user[3]}</b>\n\n"
        f"⭐ Репутация: {user[17]}\n"
        f"❤️ Лайки: {user[14]}\n"
        f"👀 Просмотры: {user[15]}\n\n"
        f"💰 Баланс: {user[12]}\n"
        f"👥 Приглашено: {user[11]}\n\n"
        f"📍 {user[4]}\n\n"
        f"{user[5]} ищет {user[6]}\n\n"
        f"📝 {user[7]}"
    )

    await message.answer_photo(
        photo=user[8],
        caption=text,
        reply_markup=profile_kb()
    )


# =======================
# ✏️ РЕДАКТОР
# =======================

@router.callback_query(lambda c: c.data == "edit")
async def edit_menu(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="edit_name")],
        [InlineKeyboardButton(text="Возраст", callback_data="edit_age")],
        [InlineKeyboardButton(text="Город", callback_data="edit_city")],
        [InlineKeyboardButton(text="О себе", callback_data="edit_about")],
        [InlineKeyboardButton(text="Фото", callback_data="edit_photo")]
    ])
    await call.message.answer("✏️ Что изменить?", reply_markup=kb)


@router.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_fields(call: CallbackQuery, state: FSMContext):
    field = call.data.split("_")[1]

    await state.set_state(getattr(EditProfile, field))
    await call.message.answer(f"Введите новое значение ({field})")


@router.message(EditProfile.name)
async def edit_name(message: Message, state: FSMContext):
    await update_field(message, state, "name", message.text)


@router.message(EditProfile.age)
async def edit_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введите число")
    await update_field(message, state, "age", int(message.text))


@router.message(EditProfile.city)
async def edit_city(message: Message, state: FSMContext):
    await update_field(message, state, "city", message.text)


@router.message(EditProfile.about)
async def edit_about(message: Message, state: FSMContext):
    await update_field(message, state, "about", message.text)


@router.message(EditProfile.photo, F.photo)
async def edit_photo(message: Message, state: FSMContext):
    await update_field(message, state, "photo", message.photo[-1].file_id)


async def update_field(message, state, field, value):
    user = get_user(message.from_user.id)

    data = {
        "name": user[2],
        "age": user[3],
        "city": user[4],
        "gender": user[5],
        "search": user[6],
        "about": user[7],
        "photo": user[8]
    }

    data[field] = value

    save_user(
        user_id=message.from_user.id,
        name=data["name"],
        age=data["age"],
        city=data["city"],
        gender=data["gender"],
        search=data["search"],
        about=data["about"],
        photo=data["photo"],
        username=message.from_user.username,
        referrer=None
    )

    await state.clear()
    await message.answer("✅ Обновлено")


# =======================
# 🖼 ГАЛЕРЕЯ (простая)
# =======================

@router.callback_query(lambda c: c.data == "gallery")
async def gallery(call: CallbackQuery):
    await call.message.answer("🖼 Галерея пока 1 фото (будет расширена)")


# =======================
# 👥 РЕФЕРАЛКА
# =======================

@router.callback_query(lambda c: c.data == "invite")
async def invite(call: CallbackQuery):
    bot_username = (await call.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={call.from_user.id}"

    await call.message.answer(
        f"👥 Приглашай друзей и получай 💰\n\n🔗 {link}"
    )


# =======================
# ❌ УДАЛЕНИЕ
# =======================

@router.callback_query(lambda c: c.data == "delete")
async def delete_profile(call: CallbackQuery):
    await call.message.answer("Точно удалить?", reply_markup=confirm_delete_kb())


@router.callback_query(lambda c: c.data == "delete_yes")
async def confirm_delete(call: CallbackQuery):
    from bot.db import cursor, conn

    cursor.execute("DELETE FROM users WHERE user_id = %s", (call.from_user.id,))
    conn.commit()

    await call.message.answer("❌ Анкета удалена")


@router.callback_query(lambda c: c.data == "delete_no")
async def cancel_delete(call: CallbackQuery):
    await call.message.answer("👌 Отмена")
