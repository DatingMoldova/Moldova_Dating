from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import save_user
from bot.keyboards.main_menu import main_menu

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()


async def start_register(message: Message, state: FSMContext = None):
    await message.answer("Как тебя зовут?")
    if state:
        await state.set_state(Reg.name)


@router.message(Reg.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Reg.age)


@router.message(Reg.age)
async def age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    data = await state.get_data()

    save_user(
        message.from_user.id,
        data["name"],
        int(message.text),
        "Город",
        "Не указано",
        "Не указано",
        "Нет описания",
        None,
        message.from_user.username,
        None
    )

    await message.answer("✅ Готово", reply_markup=main_menu)
    await state.clear()
