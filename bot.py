import logging
import os

from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BOT_NAME = "ហ្គេមស្លូត - KH"

START_TEXT = (
    f"សូមស្វាគមន៍មកកាន់ {BOT_NAME}!\n\n"
    "Your simple guide to slot-game symbols, reels, paylines, and features.\n\n"
    "Tap a button below to explore. Information and entertainment only."
)

PAGES = {
    "info": (
        f"{BOT_NAME}\n\n"
        "A simple guide to slot-game terminology and mechanics.\n\n"
        "• Learn about common symbols\n"
        "• Understand reels and paylines\n"
        "• Explore bonus features and probability\n\n"
        "This bot does not offer betting, real-money play, prizes, or cash-outs."
    ),
    "symbols": (
        "🎨 SLOT SYMBOLS\n\n"
        "Symbols are pictures or icons displayed on the reels. Common types include:\n\n"
        "🍒 Fruit — classic themed icons\n"
        "🔔 Bell — a traditional slot symbol\n"
        "⭐ Star — a common themed symbol\n"
        "7️⃣ Sevens — often used in classic-style games\n"
        "🃏 Wild — may substitute for other symbols, depending on the rules\n"
        "❓ Scatter — may trigger a feature in some games\n\n"
        "Always check the rules for the specific game; symbols do not have universal values."
    ),
    "reels": (
        "🎰 REELS & LINES\n\n"
        "Reels are the columns where symbols appear. A game may use 3, 5, or another number of reels.\n\n"
        "• Payline: a pattern that can count a symbol combination\n"
        "• Ways-to-win: a system that counts matching symbols across adjacent reels\n"
        "• Grid: the full arrangement of visible symbols\n\n"
        "Each game has its own rules. Previous results do not predict future results."
    ),
    "bonus": (
        "✨ BONUS FEATURES\n\n"
        "Some games include extra mechanics such as:\n\n"
        "• Free-spin rounds\n"
        "• Wild symbols with special behavior\n"
        "• Scatter-triggered features\n"
        "• Multipliers or expanding symbols\n\n"
        "Availability and rules vary by game. A bonus feature does not guarantee a particular outcome."
    ),
    "paylines": (
        "📐 PAYLINES EXPLAINED\n\n"
        "A payline is a predefined path across reels that a game checks for symbol combinations. "
        "Some games use fixed lines, some let players select lines, and others use ways-to-win or "
        "cluster systems instead. Read the game's information screen to see which system it uses."
    ),
    "rng": (
        "🎲 RANDOMNESS & FAIR EXPECTATIONS\n\n"
        "Many digital slot games use a random number generator (RNG) to determine outcomes. "
        "In properly designed RNG games, spins are independent: a previous result does not make "
        "a win due or predict the next result. This bot cannot predict results or guarantee wins."
    ),
    "help": (
        "ℹ️ HOW TO USE THIS BOT\n\n"
        "Tap a menu button to read about a topic. You can also use these commands:\n"
        "/start — open the main menu\n"
        "/info — about this bot\n"
        "/symbols — symbol guide\n"
        "/reels — reels and lines\n"
        "/help — show this help\n\n"
        "For information and entertainment only. No betting, real-money play, prizes, or cash-outs."
    ),
}

MENU_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🎨 Symbols", callback_data="symbols"),
        InlineKeyboardButton("🎰 Reels & Lines", callback_data="reels"),
    ],
    [
        InlineKeyboardButton("✨ Bonus Features", callback_data="bonus"),
        InlineKeyboardButton("📐 Paylines", callback_data="paylines"),
    ],
    [
        InlineKeyboardButton("🎲 RNG & Randomness", callback_data="rng"),
        InlineKeyboardButton("ℹ️ About", callback_data="info"),
    ],
    [InlineKeyboardButton("❔ Help", callback_data="help")],
])

BACK_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
    [
        InlineKeyboardButton("⬅️ Symbols", callback_data="symbols"),
        InlineKeyboardButton("➡️ Reels & Lines", callback_data="reels"),
    ],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(START_TEXT, reply_markup=MENU_KEYBOARD)


async def show_page(update: Update, context: ContextTypes.DEFAULT_TYPE, page: str) -> None:
    query = update.callback_query
    if query:
        await query.answer()
        if page == "menu":
            await query.edit_message_text(START_TEXT, reply_markup=MENU_KEYBOARD)
        else:
            await query.edit_message_text(PAGES[page], reply_markup=BACK_KEYBOARD)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    page = query.data
    if page not in PAGES and page != "menu":
        await query.answer("Unknown menu option.", show_alert=True)
        return
    await show_page(update, context, page)


async def send_page_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE, page: str
) -> None:
    if update.message:
        await update.message.reply_text(PAGES[page], reply_markup=BACK_KEYBOARD)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_page_command(update, context, "info")


async def symbols(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_page_command(update, context, "symbols")


async def reels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_page_command(update, context, "reels")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_page_command(update, context, "help")


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("start", "Open the main menu"),
        BotCommand("info", "About this bot"),
        BotCommand("symbols", "Open the symbol guide"),
        BotCommand("reels", "Learn about reels and lines"),
        BotCommand("help", "Show help"),
    ])


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
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Starting %s", BOT_NAME)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
