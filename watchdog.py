from aiogram import types, Dispatcher
import re

SENSITIVE_KEYWORDS = ["nsfw", "scam", "phishing", "xxx"]
SENSITIVE_LINKS = ["bit.ly", "tinyurl.com", "porn", "malware"]

async def watchdog_filter(message: types.Message):
    text = message.text.lower()
    flagged = False
    for word in SENSITIVE_KEYWORDS:
        if word in text:
            flagged = True
    for link in SENSITIVE_LINKS:
        if link in text:
            flagged = True
    if flagged:
        await message.delete()
        # Notify admins (placeholder: send to group)
        await message.bot.send_message(message.chat.id, f"Sensitive content detected and removed.")


def register_watchdog_handlers(dp: Dispatcher):
    dp.register_message_handler(watchdog_filter, content_types=types.ContentType.TEXT) 