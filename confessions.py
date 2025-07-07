from aiogram import types, Dispatcher
import database

# Set your target group ID here (or fetch from DB/settings)
TARGET_GROUP_ID = -1001234567890

async def handle_confession(message: types.Message):
    if message.chat.type != types.ChatType.PRIVATE:
        return
    confession = message.text
    if not confession:
        return await message.reply("Send your confession as a message to me.")
    confession_id = database.add_confession(message.from_user.id, confession, TARGET_GROUP_ID)
    await message.reply("Your confession has been sent anonymously!")
    await message.bot.send_message(
        TARGET_GROUP_ID,
        f"Confession #{confession_id}:\n{confession}"
    )

def register_confession_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_confession, content_types=types.ContentType.TEXT, chat_type=types.ChatType.PRIVATE) 