import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = BOT_TOKEN  # ← ВОТ ЭТО ДОБАВЬ

DATABASE_URL = os.getenv("DATABASE_URL")

REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

BOT_USERNAME = os.getenv("BOT_USERNAME")

LOG_CHAT_ID = int(os.getenv("LOG_CHAT_ID"))
LOG_THREAD_ID = int(os.getenv("LOG_THREAD_ID"))

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
