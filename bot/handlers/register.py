from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import create_user

router = Router()


# =========================
# 🔥 FSM
# =========================

class Register(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()


# =========================
# 🔘 КНОПКИ
# =========================

def gender_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨 Мужчина", callback_data="male"),
            InlineKeyboardButton(text="👩 Женщина", callback_data="female")
        ],
        [
            InlineKeyboardButton(text="👥 Пара", callback_data="pair"),
            InlineKeyboardButton(text="🔄 Би", callback_data="bi")
        ]
    ])


def search_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨 Мужчин", callback_data="search_male"),
            InlineKeyboardButton(text="👩 Женщин", callback_data="search_female")
        ],
        [
            InlineKeyboardButton(text="👥 Пару", callback_data="search_pair"),
            InlineKeyboardButton(text="🔄 Би", callback_data="search_bi")
        ]
    ])


def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Заново", callback_data="confirm_no")
        ]
    ])


# =========================
# 🚀 СТАРТ
# =========================

async def start_register(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👤 Введите имя:")
    await state.set_state(Register.name)


# =========================
# 👤 ИМЯ
# =========================

@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("🎂 Возраст:")
    await state.set_state(Register.age)


# =========================
# 🎂 ВОЗРАСТ
# =========================

@router.message(Register.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❌ Введите число")

    await state.update_data(age=int(message.text))
    await message.answer("📍 Город:")
    await state.set_state(Register.city)


# =========================
# 📍 ГОРОД
# =========================

@router.message(Register.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("👤 Пол:", reply_markup=gender_kb())
    await state.set_state(Register.gender)


# =========================
# 👤 ПОЛ
# =========================

@router.callback_query(Register.gender)
async def get_gender(call: CallbackQuery, state: FSMContext):
    mapping = {
        "male": "Мужчина",
        "female": "Женщина",
        "pair": "Пара",
        "bi": "Би"
    }

    await state.update_data(gender=mapping.get(call.data))
    await call.message.edit_text("❤️ Кого ищете?", reply_markup=search_kb())
    await state.set_state(Register.search)


# =========================
# ❤️ КОГО ИЩЕТ
# =========================

@router.callback_query(Register.search)
async def get_search(call: CallbackQuery, state: FSMContext):
    mapping = {
        "search_male": "Мужчин",
        "search_female": "Женщин",
        "search_pair": "Пару",
        "search_bi": "Би"
    }

    await state.update_data(search=mapping.get(call.data))
    await call.message.edit_text("📝 О себе:")
    await state.set_state(Register.about)


# =========================
# 📝 О СЕБЕ
# =========================

@router.message(Register.about)
async def get_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("📸 Фото:")
    await state.set_state(Register.photo)


# =========================
# 📸 ФОТО
# =========================

@router.message(Register.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)

    data = await state.get_data()

    text = (
        f"👤 {data['name']}, {data['age']}\n"
        f"📍 {data['city']}\n\n"
        f"{data['gender']} ищет {data['search']}\n\n"
        f"📝 {data['about']}"
    )

    await message.answer_photo(
        photo=data["photo"],
        caption=text,
        reply_markup=confirm_kb()
    )


# =========================
# ❌ НЕ ФОТО
# =========================

@router.message(Register.photo)
async def no_photo(message: Message):
    await message.answer("❌ Отправьте фото")


# =========================
# ✅ ПОДТВЕРЖДЕНИЕ (ФИКС)
# =========================

@router.callback_query(F.data.in_(["confirm_yes", "confirm_no"]))
async def confirm(call: CallbackQuery, state: FSMContext):

    if call.data == "confirm_no":
        await state.clear()
        return await call.message.edit_text("❌ Отменено")

    data = await state.get_data()

    if not data:
        return await call.message.answer("❌ Ошибка, начни заново /start")

    create_user(
        user_id=call.from_user.id,
        name=data["name"],
        age=data["age"],
        city=data["city"],
        gender=data["gender"],
        looking=data["search"],
        bio=data["about"],
        photo=data["photo"]
    )

    try:
        await call.message.delete()
    except:
        pass

    await call.message.answer_photo(
        photo=data["photo"],
        caption="✅ Анкета сохранена!"
    )

    from bot.keyboards.main_menu import main_menu

    await call.message.answer(
        "🎉 Регистрация завершена!",
        reply_markup=main_menu
    )

    await state.clear()
