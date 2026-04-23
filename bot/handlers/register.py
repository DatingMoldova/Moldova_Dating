from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import save_user, add_referral, get_user
from bot.config import LOG_CHANNEL
from bot.keyboards.main_menu import main_menu

router = Router()


class Register(StatesGroup):
    name = State()
    age = State()
    city = State()
    gender = State()
    search = State()
    about = State()
    photo = State()


async def start_register(message: Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(Register.name)


@router.message(Register.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Register.age)


@router.message(Register.age)
async def age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Register.city)


@router.message(Register.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Твой пол?")
    await state.set_state(Register.gender)


@router.message(Register.gender)
async def gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Кого ищешь?")
    await state.set_state(Register.search)


@router.message(Register.search)
async def search(message: Message, state: FSMContext):
    await state.update_data(search=message.text)
    await message.answer("Расскажи о себе")
    await state.set_state(Register.about)


@router.message(Register.about)
async def about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Отправь фото")
    await state.set_state(Register.photo)


@router.message(Register.photo, F.photo)
async def photo(message: Message, state: FSMContext, bot):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id

    referrer_id = data.get("referrer_id")

    if referrer_id and not get_user(referrer_id):
        referrer_id = None

    save_user(
        user_id=message.from_user.id,
        name=data['name'],
        age=int(data['age']),
        city=data['city'],
        gender=data['gender'],
        search=data['search'],
        about=data['about'],
        photo=photo_id,
        username=message.from_user.username,
        referrer_id=referrer_id
    )

    if referrer_id:
        add_referral(referrer_id, message.from_user.id)

    text = (
        f"💖 Moldova Dating\n\n"
        f"👤 {data['name']}, {data['age']}\n"
        f"📍 {data['city']}\n"
        f"🚻 {data['gender']} | ❤️ Ищет: {data['search']}\n\n"
        f"📝 {data['about']}\n\n"
        f"ID: {message.from_user.id}"
    )

    await bot.send_photo(LOG_CHANNEL, photo=photo_id, caption=text)

    await message.answer("✅ Анкета создана!", reply_markup=main_menu)
    await state.clear()


@router.message(Register.photo)
async def no_photo(message: Message):
    await message.answer("Отправь фото 📸")
