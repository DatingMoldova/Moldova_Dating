from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.config import REQUIRED_CHANNEL
from bot.utils.check_sub import check_subscription
from bot.handlers.register import start_register
from bot.db import get_user

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_ref(message: Message, state: FSMContext, bot):
    args = message.text.split()

    if len(args) > 1:
        referrer_id = int(args[1])

        if referrer_id != message.from_user.id:
            await state.update_data(referrer_id=referrer_id)

    await start_handler(message, state, bot)


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, bot):
    user_id = message.from_user.id

    is_sub = await check_subscription(bot, user_id, REQUIRED_CHANNEL)

    if not is_sub:
        await message.answer("Подпишись на канал и нажми /start")
        return

    user = get_user(user_id)

    if user:
        await message.answer("Ты уже зарегистрирован 👌")
        return

    await start_register(message, state)
