from aiogram import types, Dispatcher
from config import ADMIN_IDS
import database

DEFAULT_WELCOME = "Welcome, {name}!"

async def on_user_join(message: types.Message):
    user = message.new_chat_members[0]
    group_id = message.chat.id
    # Fetch custom welcome from DB or use default
    welcome_text = get_welcome_text(group_id) or DEFAULT_WELCOME
    await message.reply(welcome_text.format(name=user.full_name))
    # Assign role/tag (optional, can be expanded)
    assign_role(user.id, group_id)

async def set_welcome_text(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Only admins can set the welcome message.")
    group_id = message.chat.id
    text = message.get_args()
    if not text:
        return await message.reply("Usage: /setwelcome Welcome to the group, {name}!")
    set_welcome_text_db(group_id, text)
    await message.reply("Welcome message updated.")

# --- DB helpers (stub, to be implemented in database.py) ---
def get_welcome_text(group_id):
    # Should fetch from DB
    return None

def set_welcome_text_db(group_id, text):
    # Should save to DB
    pass

def assign_role(user_id, group_id):
    # Assign a default role/tag (expand as needed)
    pass

def register_welcome_handlers(dp: Dispatcher):
    dp.register_message_handler(set_welcome_text, commands=["setwelcome"], is_chat_admin=True)
    dp.register_message_handler(on_user_join, content_types=types.ContentType.NEW_CHAT_MEMBERS) 