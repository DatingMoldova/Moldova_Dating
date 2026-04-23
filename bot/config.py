import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL")  # @channel или id
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

BOT_USERNAME = os.getenv("BOT_USERNAME")

# 🔥 админ через Railway
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
