from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import save_user
from bot.keyboards.main_menu import main_menu
from bot.keyboards.register_kb import gender_kb, search_kb

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()


# 🔥 СТАРТ РЕГИСТРАЦИИ
async def start_reg(message: Message, state: FSMContext):
    msg = await message.answer("👤 Введите ваше имя:")

    await state.update_data(msg_id=msg.message_id)
    await state.set_state(Reg.name)


# 👤 ИМЯ
@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    data = await state.get_data()

    await state.update_data(name=message.text)

    await message.bot.edit_message_text(
        "🎂 Введите ваш возраст (16+):",
        chat_id=message.chat.id,
        message_id=data["msg_id"]
    )

    await state.set_state(Reg.age)
    await message.delete()


# 🎂 ВОЗРАСТ
@router.message(Reg.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16:
        return

    data = await state.get_data()
    await state.update_data(age=int(message.text))

    await message.bot.edit_message_text(
        "📍 Введите ваш город:",
        chat_id=message.chat.id,
        message_id=data["msg_id"]
    )

    await state.set_state(Reg.city)
    await message.delete()


# 📍 ГОРОД
@router.message(Reg.city)
async def reg_city(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(city=message.text)

    await message.bot.edit_message_text(
        "🚻 Выберите пол:",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=gender_kb
    )

    await state.set_state(Reg.gender)
    await message.delete()


# 🚻 ПОЛ
@router.message(Reg.gender)
async def reg_gender(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(gender=message.text)

    await message.bot.edit_message_text(
        "❤️ Кого ищете:",
        chat_id=message.chat.id,
        message_id=data["msg_id"],
        reply_markup=search_kb
    )

    await state.set_state(Reg.search)


# ❤️ ПОИСК
@router.message(Reg.search)
async def reg_search(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data(search=message.text)

    await message.bot.edit_message_text(
        "📝 Напишите немного о себе:",
        chat_id=message.chat.id,
        message_id=data["msg_id"]
    )

    await state.set_state(Reg.about)


# 📝 О СЕБЕ
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


# 📸 ФОТО
@router.message(Reg.photo, F.photo)
async def reg_photo(message: Message, state: FSMContext):
    data = await state.get_data()

    photo = message.photo[-1].file_id

    save_user(
        message.from_user.id,
        data["name"],
        data["age"],
        data["city"],
        data["gender"],
        data["search"],
        data["about"],
        photo,
        message.from_user.username,
        None
    )

    await message.bot.edit_message_text(
        "✅ Анкета создана!",
        chat_id=message.chat.id,
        message_id=data["msg_id"]
    )

    await message.answer("Главное меню 👇", reply_markup=main_menu)

    await state.clear()
    await message.delete()
