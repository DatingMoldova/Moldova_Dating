from bot.handlers import register, profile, admin

def setup_routers(dp):
    dp.include_router(register.router)
    dp.include_router(profile.router)
    dp.include_router(admin.router)
