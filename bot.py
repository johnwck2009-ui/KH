import logging
import os

from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BOT_NAME = "ហ្គេមស្លូត - KH"

START_TEXT = (
    f"សូមស្វាគមន៍មកកាន់ {BOT_NAME}!\n\n"
    "This bot shares information about slot games, symbols, reels, and game mechanics.\n\n"
    "Choose a command to learn more. Information and entertainment only."
)

SYMBOLS_TEXT = (
    "Slot symbols are pictures or icons shown on the reels. Common examples include "
    "fruits, bells, stars, numbers, and themed characters. Their meaning and value "
    "depend on the rules of each individual game."
)

REELS_TEXT = (
    "Reels are the columns that display symbols in a slot game. When a round ends, "
    "the visible symbols form a result. Paylines, ways-to-win systems, and bonus "
    "features vary by game. Outcomes are random in games designed around random "
    "number generators; past results do not predict future results."
)

INFO_TEXT = (
    f"{BOT_NAME}\n\n"
    "A simple guide to slot-game terminology and mechanics.\n\n"
    "• Learn about common symbols\n"
    "• Understand reels and paylines\n"
    "• Explore bonus features and basic terminology\n\n"
    "For information and entertainment only. This bot does not offer betting, "
    "real-money play, prizes, or cash-outs."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(START_TEXT)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(INFO_TEXT)


async def symbols(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(SYMBOLS_TEXT)


async def reels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(REELS_TEXT)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Available commands:\n"
            "/start - Start the bot\n"
            "/info - About this bot\n"
            "/symbols - Learn about slot symbols\n"
            "/reels - Learn how reels work\n"
            "/help - Show this help message"
        )


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Start the bot"),
            BotCommand("info", "About this bot"),
            BotCommand("symbols", "Learn about slot symbols"),
            BotCommand("reels", "Learn how reels work"),
            BotCommand("help", "Show help"),
        ]
    )


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Missing TELEGRAM_BOT_TOKEN environment variable. "
            "Create a bot with @BotFather and set its token as an environment secret."
        )

    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("symbols", symbols))
    application.add_handler(CommandHandler("reels", reels))
    application.add_handler(CommandHandler("help", help_command))

    logger.info("Starting %s", BOT_NAME)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
