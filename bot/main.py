import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.loader import setup_routers
from bot.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    try:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )

        dp = Dispatcher()

        setup_routers(dp)

        print("🚀 Bot started")

        await dp.start_polling(bot)

    except Exception as e:
        print("💥 ERROR:", e)


if __name__ == "__main__":
    asyncio.run(main())
