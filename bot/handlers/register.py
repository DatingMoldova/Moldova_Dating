from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import save_user
from bot.keyboards.register_kb import gender_kb, search_kb
from bot.keyboards.main_menu import main_menu

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()


async def start_register(message: Message):
    await message.answer("Как тебя зовут?")
    await Reg.name.set()


@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Reg.age)


@router.message(Reg.age)
async def age(message: Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) < 16:
        await message.answer("Только 16+")
        return

    await state.update_data(age=int(message.text))
    await message.answer("Твой город?")
    await state.set_state(Reg.city)


@router.message(Reg.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Выбери пол 👇", reply_markup=gender_kb)
    await state.set_state(Reg.gender)


@router.message(Reg.gender)
async def gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Кого ищешь 👇", reply_markup=search_kb)
    await state.set_state(Reg.search)


@router.message(Reg.search)
async def search(message: Message, state: FSMContext):
    await state.update_data(search=message.text)
    await message.answer("Напиши о себе")
    await state.set_state(Reg.about)


@router.message(Reg.about)
async def about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Отправь фото")
    await state.set_state(Reg.photo)


@router.message(Reg.photo, F.photo)
async def photo(message: Message, state: FSMContext):
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

    await message.answer("✅ Регистрация завершена", reply_markup=main_menu)
    await state.clear()
