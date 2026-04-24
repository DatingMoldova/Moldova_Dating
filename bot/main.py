import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.loader import setup_routers
from bot.config import TOKEN

logging.basicConfig(level=logging.INFO)

async def main():
    try:
        bot = Bot(token=TOKEN, parse_mode="HTML")
        dp = Dispatcher()

        setup_routers(dp)

        print("🚀 Bot started")
        await dp.start_polling(bot)

    except Exception as e:
        print("💥 ERROR:", e)

if __name__ == "__main__":
    asyncio.run(main())
