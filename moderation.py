from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
import re
from config import ADMIN_IDS

# Profanity and link patterns (expand as needed)
PROFANITY_LIST = ["badword1", "badword2"]
LINK_PATTERN = re.compile(r"https?://|www\.")

# --- Moderation Commands ---
async def ban_user(message: types.Message):
    if not await is_admin(message):
        return await message.reply("You need to be an admin to use this command.")
    if not message.reply_to_message:
        return await message.reply("Reply to a user to ban them.")
    try:
        await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply("User banned.")
    except BadRequest:
        await message.reply("Failed to ban user.")

async def kick_user(message: types.Message):
    if not await is_admin(message):
        return await message.reply("You need to be an admin to use this command.")
    if not message.reply_to_message:
        return await message.reply("Reply to a user to kick them.")
    try:
        await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply("User kicked.")
    except BadRequest:
        await message.reply("Failed to kick user.")

async def mute_user(message: types.Message):
    if not await is_admin(message):
        return await message.reply("You need to be an admin to use this command.")
    if not message.reply_to_message:
        return await message.reply("Reply to a user to mute them.")
    try:
        await message.bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            types.ChatPermissions(can_send_messages=False)
        )
        await message.reply("User muted.")
    except BadRequest:
        await message.reply("Failed to mute user.")

async def unmute_user(message: types.Message):
    if not await is_admin(message):
        return await message.reply("You need to be an admin to use this command.")
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unmute them.")
    try:
        await message.bot.restrict_chat_member(
            message.chat.id,
            message.reply_to_message.from_user.id,
            types.ChatPermissions(can_send_messages=True,
                                  can_send_media_messages=True,
                                  can_send_other_messages=True,
                                  can_add_web_page_previews=True)
        )
        await message.reply("User unmuted.")
    except BadRequest:
        await message.reply("Failed to unmute user.")

# --- Filters ---
async def filter_messages(message: types.Message):
    # Profanity filter
    if any(word in message.text.lower() for word in PROFANITY_LIST):
        await message.delete()
        return
    # Link filter
    if LINK_PATTERN.search(message.text):
        await message.delete()
        return
    # Spam protection (simple: repeated chars/words)
    if len(set(message.text.lower().split())) == 1 or message.text.count(message.text[0]) > 10:
        await message.delete()
        return

async def is_admin(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        return True
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.is_chat_admin()

# --- Register Handlers ---
def register_moderation_handlers(dp: Dispatcher):
    dp.register_message_handler(ban_user, Command("ban"), commands_prefix="/", is_chat_admin=True)
    dp.register_message_handler(kick_user, Command("kick"), commands_prefix="/", is_chat_admin=True)
    dp.register_message_handler(mute_user, Command("mute"), commands_prefix="/", is_chat_admin=True)
    dp.register_message_handler(unmute_user, Command("unmute"), commands_prefix="/", is_chat_admin=True)
    dp.register_message_handler(filter_messages, content_types=types.ContentType.TEXT, is_chat_admin=False, state="*") 