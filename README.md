# ហ្គេមស្លូត - KH

A standard Telegram bot with clickable inline buttons and educational pages about slot-game symbols, reels, paylines, bonus features, and randomness. It is **not** a Telegram Mini App and does not provide betting, real-money play, prizes, or cash-outs.

## Interactive menu

Send `/start` to display buttons for:
- 🎨 Symbols
- 🎰 Reels & Lines
- ✨ Bonus Features
- 📐 Paylines
- 🎲 RNG & Randomness
- ℹ️ About
- ❔ Help

Each button opens a topic page. Topic pages include a Main Menu button and quick navigation buttons.

## Commands

- `/start` — Open the main menu
- `/info` — About the bot
- `/symbols` — Learn about common slot symbols
- `/reels` — Learn how reels and lines work
- `/help` — Show available commands

## Run locally

1. Create a Telegram bot using [@BotFather](https://t.me/BotFather).
2. Copy the bot token from BotFather. Keep it private; do not commit it to GitHub.
3. Install Python 3.10 or newer.
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set the token as an environment variable.

   macOS/Linux:
   ```bash
   export TELEGRAM_BOT_TOKEN="paste-your-token-here"
   python bot.py
   ```

   Windows PowerShell:
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="paste-your-token-here"
   python bot.py
   ```

## Keep it running

Deploy the project to a Python-compatible hosting service and add `TELEGRAM_BOT_TOKEN` as a private environment secret. Run command: `python bot.py`. A continuously running worker is needed for polling. If already deployed, redeploy/restart the service after pulling the latest commit so the new buttons become available.

## Telegram profile text

**Description:** Learn about slot games, symbols, reels, and game mechanics in one place.

**About:** Slot game information and facts.
