from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from config import ADMIN_IDS
import database

WARNING_THRESHOLD = 3  # Number of warnings before action

async def warn_user(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Only admins can issue warnings.")
    if not message.reply_to_message:
        return await message.reply("Reply to a user to warn them.")
    user_id = message.reply_to_message.from_user.id
    group_id = message.chat.id
    count = database.add_warning(user_id, group_id)
    await message.reply(f"User warned. Total warnings: {count}")
    if count >= WARNING_THRESHOLD:
        # Mute or ban user
        await message.bot.restrict_chat_member(
            group_id,
            user_id,
            types.ChatPermissions(can_send_messages=False)
        )
        await message.reply(f"User muted for exceeding {WARNING_THRESHOLD} warnings.")

async def warnings_count(message: types.Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a user to check warnings.")
    user_id = message.reply_to_message.from_user.id
    group_id = message.chat.id
    count = database.get_warning_count(user_id, group_id)
    await message.reply(f"User has {count} warnings.")

def register_warn_handlers(dp: Dispatcher):
    dp.register_message_handler(warn_user, Command("warn"), is_chat_admin=True)
    dp.register_message_handler(warnings_count, Command("warnings"), is_chat_admin=True) 