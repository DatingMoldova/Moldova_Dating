from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import save_user, get_user
from bot.utils.logger import log_profile

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


# 🔥 СТЕЙТЫ
class Register(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()
    confirm = State()


# 🔘 КНОПКИ
def gender_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Парень", callback_data="male"),
                InlineKeyboardButton(text="👩 Девушка", callback_data="female")
            ]
        ]
    )


def search_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👨 Парней", callback_data="search_male"),
                InlineKeyboardButton(text="👩 Девушек", callback_data="search_female")
            ]
        ]
    )


def confirm_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="confirm_no")
            ]
        ]
    )


# 🚀 СТАРТ РЕГИСТРАЦИИ
@router.message(F.text == "🚀 Регистрация")
async def start_register(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("👤 Введите ваше имя:")
    await state.set_state(Register.name)


# 👤 ИМЯ
@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🎂 Введите возраст:")
    await state.set_state(Register.age)


# 🎂 ВОЗРАСТ
@router.message(Register.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введите число")

    await state.update_data(age=int(message.text))
    await message.answer("📍 Ваш город:")
    await state.set_state(Register.city)


# 📍 ГОРОД
@router.message(Register.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("👤 Ваш пол:", reply_markup=gender_kb())
    await state.set_state(Register.gender)


# 👤 ПОЛ
@router.callback_query(Register.gender)
async def get_gender(call: CallbackQuery, state: FSMContext):
    gender = "Парень" if call.data == "male" else "Девушка"

    await state.update_data(gender=gender)
    await call.message.edit_text("❤️ Кого ищете?", reply_markup=search_kb())
    await state.set_state(Register.search)


# ❤️ КОГО ИЩЕМ
@router.callback_query(Register.search)
async def get_search(call: CallbackQuery, state: FSMContext):
    search = "Парней" if call.data == "search_male" else "Девушек"

    await state.update_data(search=search)
    await call.message.edit_text("📝 Расскажите о себе:")
    await state.set_state(Register.about)


# 📝 О СЕБЕ
@router.message(Register.about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("📸 Отправьте фото:")
    await state.set_state(Register.photo)


# 📸 ФОТО
@router.message(Register.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()

    text = (
        "📋 <b>Проверьте анкету</b>\n\n"

        f"👤 {data['name']}, {data['age']}\n"
        f"📍 {data['city']}\n\n"
        f"{data['gender']} ищет {data['search']}\n\n"
        f"📝 {data['about']}"
    )

    await message.answer_photo(
        photo=photo_id,
        caption=text,
        reply_markup=confirm_kb()
    )

    await state.set_state(Register.confirm)


# ❌ ЕСЛИ НЕ ФОТО
@router.message(Register.photo)
async def no_photo(message: Message):
    await message.answer("❌ Отправьте фото")


# ✅ ПОДТВЕРЖДЕНИЕ
@router.callback_query(Register.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    if call.data == "confirm_no":
        await state.clear()
        return await call.message.edit_text("❌ Регистрация отменена")

    data = await state.get_data()

    save_user(
        user_id=call.from_user.id,
        name=data["name"],
        age=data["age"],
        city=data["city"],
        gender=data["gender"],
        search=data["search"],
        about=data["about"],
        photo=data["photo"],
        username=call.from_user.username,
        referrer=None
    )

    # 🔥 ЛОГ В ГРУППУ
    user = get_user(call.from_user.id)
    await log_profile(call.bot, user)

    await state.clear()

    await call.message.edit_text("✅ Анкета сохранена!")
