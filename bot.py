import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN

# Import feature modules (to be implemented)
# from moderation import register_moderation_handlers
# from games import register_game_handlers
# from ai_assistant import register_ai_handlers
# from welcome import register_welcome_handlers
# ... add more as needed

def setup_handlers(dp: Dispatcher):
    # Register handlers from each module
    # register_moderation_handlers(dp)
    # register_game_handlers(dp)
    # register_ai_handlers(dp)
    # register_welcome_handlers(dp)
    # ... add more as needed
    pass

async def on_startup(dispatcher):
    logging.info("Bot is starting up...")

async def on_shutdown(dispatcher):
    logging.info("Bot is shutting down...")

def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot)

    setup_handlers(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == "__main__":
    main() 