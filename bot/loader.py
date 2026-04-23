from aiogram import Dispatcher

# 🔥 все роутеры
from bot.handlers.start import router as start_router
from bot.handlers.register import router as register_router
from bot.handlers.profile import router as profile_router
from bot.handlers.agreement import router as agreement_router
from bot.handlers.menu import router as menu_router
from bot.handlers.about import router as about_router
from bot.handlers.help import router as help_router


def setup_routers(dp: Dispatcher):
    # 🔥 порядок важен
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)

    dp.include_router(agreement_router)
    dp.include_router(about_router)
    dp.include_router(help_router)
    dp.include_router(menu_router)
