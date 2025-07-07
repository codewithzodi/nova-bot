# config.py
# Add your Telegram bot token here

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TRANSLATE_API_KEY = os.getenv("TRANSLATE_API_KEY", "")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///nova_bot.db")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()] 