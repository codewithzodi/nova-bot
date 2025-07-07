from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from config import ADMIN_IDS
import database

async def add_custom_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Only admins can add custom commands.")
    args = message.get_args().split(" ", 1)
    if len(args) < 2:
        return await message.reply("Usage: /addcommand command_name response_text")
    command, response = args[0].lower(), args[1]
    database.set_custom_command(message.chat.id, command, response)
    await message.reply(f"Custom command /{command} added.")

async def remove_custom_command(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return await message.reply("Only admins can remove custom commands.")
    command = message.get_args().strip().lower()
    if not command:
        return await message.reply("Usage: /removecommand command_name")
    database.remove_custom_command(message.chat.id, command)
    await message.reply(f"Custom command /{command} removed.")

async def handle_custom_command(message: types.Message):
    command = message.text.lstrip("/").split()[0].lower()
    response = database.get_custom_command(message.chat.id, command)
    if response:
        await message.reply(response)

def register_custom_command_handlers(dp: Dispatcher):
    dp.register_message_handler(add_custom_command, Command("addcommand"), is_chat_admin=True)
    dp.register_message_handler(remove_custom_command, Command("removecommand"), is_chat_admin=True)
    dp.register_message_handler(handle_custom_command, lambda m: m.text and m.text.startswith("/")) 