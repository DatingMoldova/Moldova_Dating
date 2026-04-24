from bot.handlers.start import router as start_router
from bot.handlers.register import router as register_router
from bot.handlers.profile import router as profile_router
from bot.handlers.admin import router as admin_router

def setup_routers(dp):
    dp.include_router(start_router)
    dp.include_router(register_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)
