from aiogram import types, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import database
from datetime import datetime
import re

scheduler = AsyncIOScheduler()

async def add_event(message: types.Message):
    args = message.get_args()
    match = re.match(r"(.+)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", args)
    if not match:
        return await message.reply("Usage: /add_event EventName YYYY-MM-DD HH:MM")
    event, time_str = match.groups()
    try:
        event_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return await message.reply("Invalid date format. Use YYYY-MM-DD HH:MM")
    database.add_event(message.from_user.id, message.chat.id, event, event_time)
    scheduler.add_job(send_event_reminder, 'date', run_date=event_time, args=[message.chat.id, event])
    await message.reply(f"Event '{event}' scheduled for {event_time}.")

async def send_event_reminder(chat_id, event):
    # This function is called by the scheduler
    # You may need to pass the bot instance if not globally available
    from bot import main  # or pass bot instance another way
    # This is a placeholder; actual implementation may differ
    # await bot.send_message(chat_id, f"Reminder: {event}")
    pass

def register_event_handlers(dp: Dispatcher):
    dp.register_message_handler(add_event, commands=["add_event"])
    scheduler.start() 