# 🚀 NovaBot: The Next-Gen AI Telegram Group Bot

Welcome to **NovaBot** – your all-in-one, AI-powered Telegram group assistant! NovaBot keeps your group safe, fun, and lively with smart moderation, engaging games, anonymous confessions, and much more. Whether you're running a study group, a meme squad, or a professional community, NovaBot adapts to your vibe and makes every chat better.

---

## ✨ Features

- 🛡️ **Moderation Tools**: `/ban`, `/kick`, `/mute`, `/unmute`, spam & link filters, profanity filter, auto-delete rules
- 👋 **Welcome & Roles**: Auto-greet new users, assign custom roles/tags
- ⚠️ **Warn System**: Admin warnings, thresholds for mute/ban, customizable messages
- 📝 **Custom Commands**: Admin-defined commands like `/rules`, `/about`, `/links`
- 🤖 **AI Assistant**: OpenAI-powered chat, jokes, meme generation, toggleable per group
- 🎭 **Anonymous Confessions**: DM the bot, posted anonymously in group
- 🎮 **Mini Games**: Trivia, emoji guessing, reaction speed, leaderboard
- 🌍 **Auto Translation**: Detects and translates messages to group's language
- 💌 **Compliment Mode**: Sends random compliments to users
- 🧩 **Daily Puzzle**: Posts riddles, tracks answers and scores
- 🎨 **Themeable Personality**: Switch between friendly, sarcastic, professional, etc.
- 📅 **Events & Reminders**: Set birthdays, deadlines, group events
- 🔒 **Sensitive Content Watchdog**: AI-powered content scanning and flagging

---

## 🛠️ Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/codewithzodi/nova-bot.git
   cd nova-bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Fill in your secrets in `.env` (see comments in the file).
4. **Initialize the database:**
   - Add this to the top of your `main()` in `bot.py`:
     ```python
     from database import init_db
     init_db()
     ```
5. **Run the bot:**
   ```bash
   python bot.py
   ```
6. **Add NovaBot to your Telegram group and make it admin!**

---

## 💡 Usage Tips

- Type `/help` in your group to see what NovaBot can do.
- Admins can configure features and custom commands directly from chat.
- Try `/setpersonality friendly` or `/setpersonality sarcastic` for a new vibe!
- Use `/add_event Birthday 2024-12-31 18:00` to schedule reminders.
- DM the bot for anonymous confessions – your secret's safe!
- Compete in games and check `/leaderboard` for the top scorers.

---

## 🤝 Contributing

NovaBot is open to contributions! Feel free to fork, submit pull requests, or suggest features. Check the issues tab for ideas or to report bugs.

---

## 👨‍💻 Developer Credits
- **Project Lead:** [@CodeWithZodi](https://github.com/codewithzodi)
📩 mailzodibhai@gmail.com
- **Contributors:** NONE RIGHT NOW

---

## 📄 License
MIT License

---

> **NovaBot** – Making every group smarter, safer, and more fun! ✨ 
