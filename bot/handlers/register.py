from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.db import create_user
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
    confirm = State()


def gender_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨", callback_data="male"),
         InlineKeyboardButton(text="👩", callback_data="female")]
    ])


def search_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨", callback_data="search_male"),
         InlineKeyboardButton(text="👩", callback_data="search_female")]
    ])


def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅", callback_data="confirm_yes"),
         InlineKeyboardButton(text="❌", callback_data="confirm_no")]
    ])


@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите имя:")
    await state.set_state(Register.name)


@router.message(Register.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Возраст:")
    await state.set_state(Register.age)


@router.message(Register.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Город:")
    await state.set_state(Register.city)


@router.message(Register.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Пол:", reply_markup=gender_kb())
    await state.set_state(Register.gender)


@router.callback_query(Register.gender)
async def gender(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(gender=call.data)
    await call.message.edit_text("Кого ищешь?", reply_markup=search_kb())
    await state.set_state(Register.search)


@router.callback_query(Register.search)
async def search(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(search=call.data)
    await call.message.edit_text("О себе:")
    await state.set_state(Register.about)


@router.message(Register.about)
async def about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await message.answer("Фото:")
    await state.set_state(Register.photo)


@router.message(Register.photo, F.photo)
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)

    data = await state.get_data()

    await message.answer_photo(
        photo=data["photo"],
        caption="Проверь анкету",
        reply_markup=confirm_kb()
    )

    await state.set_state(Register.confirm)


@router.callback_query(Register.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    await call.answer()

    if call.data == "confirm_no":
        await state.clear()
        return await call.message.edit_text("Отменено")

    data = await state.get_data()

    create_user(
        call.from_user.id,
        data["name"],
        data["age"],
        data["city"],
        data["gender"],
        data["search"],
        data["about"],
        data["photo"]
    )

    await call.message.delete()

    await call.message.answer("✅ Готово", reply_markup=main_menu())

    await state.clear()
