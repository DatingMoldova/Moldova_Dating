import asyncio
from aiogram import Bot, Dispatcher
from bot.loader import setup_routers
from bot.config import TOKEN

async def main():
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    setup_routers(dp)

    print("🚀 Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
