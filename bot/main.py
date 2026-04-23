import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.db import init_db

from bot.handlers.start import router as start_router
from bot.handlers.register import router as register_router
from bot.handlers.menu import router as menu_router
from bot.handlers.admin import router as admin_router


async def main():
    logging.basicConfig(level=logging.INFO)

    # 🔥 БД
    init_db()

    # 🔥 БОТ (новый способ)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # 🔥 ДИСПЕТЧЕР
    dp = Dispatcher()

    # 🔥 РОУТЕРЫ (ВАЖНО!)
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(menu_router)
    dp.include_router(admin_router)

    # 🔥 фикс "бот не отвечает"
    await bot.delete_webhook(drop_pending_updates=True)

    print("🚀 Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
