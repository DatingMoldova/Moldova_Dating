from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import save_user
from bot.keyboards.main_menu import main_menu
from bot.keyboards.register_kb import gender_kb, search_kb, back_kb, confirm_kb

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()


def step(text, num):
    return f"📋 Шаг {num}/6\n\n{text}"


# 🚀 старт
async def start_reg(message: Message, state: FSMContext):
    msg = await message.answer(step("👤 Введите ваше имя:", 1))
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Reg.name)


# 👤 имя
@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.update_data(name=message.text)

    await message.bot.edit_message_text(
        step("🎂 Введите возраст (16+):", 2),
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=back_kb()
    )

    await state.set_state(Reg.age)
    await message.delete()


# 🎂 возраст
@router.message(Reg.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16:
        await message.answer("❌ Введите корректный возраст (16+)")
        return

    data = await state.get_data()
    await state.update_data(age=int(message.text))

    await message.bot.edit_message_text(
        step("📍 Введите город:", 3),
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=back_kb()
    )

    await state.set_state(Reg.city)
    await message.delete()


# 📍 город
@router.message(Reg.city)
async def reg_city(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(city=message.text)

    await message.bot.edit_message_text(
        step("🚻 Выберите пол:", 4),
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=gender_kb()
    )

    await state.set_state(Reg.gender)
    await message.delete()


# 🚻 пол
@router.callback_query(Reg.gender)
async def reg_gender(call: CallbackQuery, state: FSMContext):
    await call.answer()

    mapping = {
        "g_male": "👨 Мужчина",
        "g_female": "👩 Женщина",
        "g_pair": "👫 Пара",
        "g_bi": "⚧ Би"
    }

    if call.data not in mapping:
        return

    await state.update_data(gender=mapping[call.data])

    await call.message.edit_text(
        step("❤️ Кого ищете:", 5),
        reply_markup=search_kb()
    )

    await state.set_state(Reg.search)


# ❤️ поиск
@router.callback_query(Reg.search)
async def reg_search(call: CallbackQuery, state: FSMContext):
    await call.answer()

    mapping = {
        "s_male": "👨 Мужчину",
        "s_female": "👩 Девушку",
        "s_pair": "👫 Пару",
        "s_bi": "⚧ Би",
        "s_all": "🌍 Всех"
    }

    if call.data not in mapping:
        return

    await state.update_data(search=mapping[call.data])

    await call.message.edit_text(
        step("📝 Напишите о себе:", 6),
        reply_markup=back_kb()
    )

    await state.set_state(Reg.about)


# 📝 о себе
@router.message(Reg.about)
async def reg_about(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(about=message.text)

    await message.bot.edit_message_text(
        "📸 Отправьте фото:",
        chat_id=message.chat.id,
        message_id=data["msg_id"]
    )

    await state.set_state(Reg.photo)
    await message.delete()


# 📸 фото → ПРЕДПРОСМОТР
@router.message(Reg.photo)
async def reg_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("❌ Отправьте фото")
        return

    data = await state.get_data()

    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)

    text = (
        f"👤 {data.get('name')}, {data.get('age')}\n"
        f"📍 {data.get('city')}\n\n"
        f"{data.get('gender')} → {data.get('search')}\n\n"
        f"📝 {data.get('about')}"
    )

    await message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=confirm_kb()
    )

    await message.delete()


# ✅ подтвердить
@router.callback_query(F.data == "confirm_yes")
async def confirm_yes(call: CallbackQuery, state: FSMContext):
    await call.answer()

    try:
        data = await state.get_data()

        save_user(
            call.from_user.id,
            data.get("name"),
            data.get("age"),
            data.get("city"),
            data.get("gender"),
            data.get("search"),
            data.get("about"),
            data.get("photo"),
            call.from_user.username,
            None
        )

        await call.message.delete()

        await call.message.answer(
            "✅ Анкета сохранена!",
            reply_markup=main_menu
        )

        await state.clear()

    except Exception as e:
        await call.message.answer(f"❌ Ошибка: {e}")


# ❌ заново
@router.callback_query(F.data == "confirm_no")
async def confirm_no(call: CallbackQuery, state: FSMContext):
    await call.answer()

    await state.clear()
    await call.message.delete()

    await call.message.answer("🔄 Начнём заново")

    from bot.handlers.register import start_reg
    await start_reg(call.message, state)


# ⬅️ назад
@router.callback_query(F.data == "back")
async def go_back(call: CallbackQuery, state: FSMContext):
    await call.answer()

    current = await state.get_state()

    if current == Reg.age.state:
        await state.set_state(Reg.name)
        await call.message.edit_text(step("👤 Введите имя:", 1))

    elif current == Reg.city.state:
        await state.set_state(Reg.age)
        await call.message.edit_text(step("🎂 Введите возраст:", 2), reply_markup=back_kb())

    elif current == Reg.gender.state:
        await state.set_state(Reg.city)
        await call.message.edit_text(step("📍 Введите город:", 3), reply_markup=back_kb())

    elif current == Reg.search.state:
        await state.set_state(Reg.gender)
        await call.message.edit_text(step("🚻 Выберите пол:", 4), reply_markup=gender_kb())

    elif current == Reg.about.state:
        await state.set_state(Reg.search)
        await call.message.edit_text(step("❤️ Кого ищете:", 5), reply_markup=search_kb())
