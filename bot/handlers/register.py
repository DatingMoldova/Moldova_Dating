from aiogram import Router, F
from aiogram.types import Message
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


# 👤 ИМЯ
@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Сколько тебе лет?")
    await state.set_state(Reg.age)


# 🎂 ВОЗРАСТ
@router.message(Reg.age)
async def reg_age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16:
        await message.answer("Только 16+")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Твой город?")
    await state.set_state(Reg.city)


# 📍 ГОРОД
@router.message(Reg.city)
async def reg_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)

    await message.answer("Выбери пол 👇", reply_markup=gender_kb)
    await state.set_state(Reg.gender)


# 🚻 ПОЛ
@router.message(Reg.gender)
async def reg_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)

    await message.answer("Кого ищешь 👇", reply_markup=search_kb)
    await state.set_state(Reg.search)


# ❤️ КОГО ИЩЕШЬ
@router.message(Reg.search)
async def reg_search(message: Message, state: FSMContext):
    await state.update_data(search=message.text)

    await message.answer("Напиши о себе")
    await state.set_state(Reg.about)


# 📝 О СЕБЕ
@router.message(Reg.about)
async def reg_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    await message.answer("Отправь фото")
    await state.set_state(Reg.photo)


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

    await message.answer("✅ Анкета создана!", reply_markup=main_menu)
    await state.clear()
