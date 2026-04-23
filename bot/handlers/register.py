from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.db import save_user
from bot.keyboards.main_menu import main_menu

router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()


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

    data = await state.get_data()

    save_user(
        message.from_user.id,
        data["name"],
        int(message.text),
        "Не указан",
        "Не указан",
        "Не указан",
        "Без описания",
        None,
        message.from_user.username,
        None
    )

    await message.answer("✅ Регистрация завершена", reply_markup=main_menu)
    await state.clear()
