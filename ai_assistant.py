from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from config import OPENAI_API_KEY
import openai
import re

openai.api_key = OPENAI_API_KEY

async def ai_ask(message: types.Message):
    prompt = message.get_args() or (message.reply_to_message.text if message.reply_to_message else None)
    if not prompt:
        return await message.reply("Please provide a question or reply to a message.")
    response = await ask_openai(prompt)
    await message.reply(response)

async def ai_tagged(message: types.Message):
    # Respond if bot is tagged in a group
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention" and message.text[entity.offset:entity.offset+entity.length].lower() in ["@novabot", "@yourbotusername"]:
                prompt = message.text.replace(f"@{message.bot.username}", "").strip()
                response = await ask_openai(prompt)
                await message.reply(response)
                break

async def ask_openai(prompt):
    try:
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"AI error: {e}"

def register_ai_handlers(dp: Dispatcher):
    dp.register_message_handler(ai_ask, Command("ask"))
    dp.register_message_handler(ai_tagged, lambda m: m.text and re.search(r"@novabot|@yourbotusername", m.text, re.I)) 