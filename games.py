from aiogram import types, Dispatcher
import random
import database

TRIVIA_QUESTIONS = [
    {"q": "What is the capital of France?", "a": "paris"},
    {"q": "2 + 2 = ?", "a": "4"},
    {"q": "What color is the sky?", "a": "blue"},
]
EMOJIS = ["😀", "🎉", "🚀", "🐱", "🍕"]

current_trivia = {}
current_emoji = {}
current_tap = {}

async def trivia(message: types.Message):
    q = random.choice(TRIVIA_QUESTIONS)
    current_trivia[message.chat.id] = q
    await message.reply(f"Trivia: {q['q']}")

async def answer_trivia(message: types.Message):
    q = current_trivia.get(message.chat.id)
    if not q:
        return
    if message.text.strip().lower() == q["a"]:
        database.add_score(message.from_user.id, message.chat.id, 1)
        await message.reply("Correct! +1 point.")
        del current_trivia[message.chat.id]
    else:
        await message.reply("Incorrect. Try again!")

async def guess_emoji(message: types.Message):
    emoji = random.choice(EMOJIS)
    current_emoji[message.chat.id] = emoji
    await message.reply(f"Guess the emoji: {emoji}")

async def answer_emoji(message: types.Message):
    emoji = current_emoji.get(message.chat.id)
    if not emoji:
        return
    if message.text.strip() == emoji:
        database.add_score(message.from_user.id, message.chat.id, 1)
        await message.reply("You guessed it! +1 point.")
        del current_emoji[message.chat.id]

async def tap(message: types.Message):
    current_tap[message.chat.id] = True
    await message.reply("First to reply with 'tap' wins!")

async def answer_tap(message: types.Message):
    if current_tap.get(message.chat.id) and message.text.strip().lower() == "tap":
        database.add_score(message.from_user.id, message.chat.id, 1)
        await message.reply(f"{message.from_user.full_name} wins! +1 point.")
        del current_tap[message.chat.id]

async def leaderboard(message: types.Message):
    scores = database.get_leaderboard(message.chat.id)
    if not scores:
        return await message.reply("No scores yet.")
    text = "Leaderboard:\n" + "\n".join([f"{u}: {s}" for u, s in scores])
    await message.reply(text)

def register_game_handlers(dp: Dispatcher):
    dp.register_message_handler(trivia, commands=["trivia"])
    dp.register_message_handler(answer_trivia, lambda m: m.chat.id in current_trivia)
    dp.register_message_handler(guess_emoji, commands=["emoji"])
    dp.register_message_handler(answer_emoji, lambda m: m.chat.id in current_emoji)
    dp.register_message_handler(tap, commands=["tap"])
    dp.register_message_handler(answer_tap, lambda m: m.chat.id in current_tap)
    dp.register_message_handler(leaderboard, commands=["leaderboard"]) 