import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.db import init_db
from bot.loader import setup_routers


async def main():
    logging.basicConfig(level=logging.INFO)

    # 🔥 БД
    init_db()

    # 🔥 БОТ
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # 🔥 ДИСПЕТЧЕР
    dp = Dispatcher()

    # 🔥 ПОДКЛЮЧЕНИЕ ВСЕГО
    setup_routers(dp)

    # 🔥 фикс зависаний
    await bot.delete_webhook(drop_pending_updates=True)

    print("🚀 Бот запущен")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
