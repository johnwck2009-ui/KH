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

BOT_NAME = "Khmer Slot Guide - KH"

START_TEXT = (
    f"សូមស្វាគមន៍មកកាន់ {BOT_NAME}!\n\n"
    "ស្វែងយល់អំពីនិមិត្តសញ្ញា ស្គ្រីនវិល បន្ទាត់ឈ្នះ និងមុខងារផ្សេងៗ "
    "ក្នុងហ្គេមស្លូត តាមរយៈការណែនាំងាយៗ។\n\n"
    "សូមចុចប៊ូតុងខាងក្រោម ដើម្បីជ្រើសរើសប្រធានបទ។\n\n"
    "សម្រាប់ព័ត៌មាន និងចំណេះដឹងប៉ុណ្ណោះ។"
)

PAGES = {
    "info": (
        f"{BOT_NAME}\n\n"
        "បូតនេះផ្តល់ព័ត៌មានអំពីពាក្យបច្ចេកទេស និងរបៀបដំណើរការរបស់ហ្គេមស្លូត។\n\n"
        "• ស្វែងយល់អំពីនិមិត្តសញ្ញាទូទៅ\n"
        "• យល់ដឹងអំពីស្គ្រីនវិល និងបន្ទាត់ឈ្នះ\n"
        "• ស្វែងយល់អំពីមុខងារបន្ថែម និងប្រូបាប៊ីលីតេ\n\n"
        "បូតនេះមិនផ្តល់សេវាភ្នាល់ ការលេងដោយប្រើប្រាក់ពិត រង្វាន់ ឬការដកប្រាក់ទេ។"
    ),
    "symbols": (
        "🎨 និមិត្តសញ្ញាក្នុងហ្គេមស្លូត\n\n"
        "និមិត្តសញ្ញា គឺជារូបភាព ឬរូបតំណាងដែលបង្ហាញនៅលើស្គ្រីនវិល។ ឧទាហរណ៍៖\n\n"
        "🍒 ផ្លែឈើ — រូបតំណាងដែលគេឃើញក្នុងហ្គេមបែបបុរាណ\n"
        "🔔 កណ្ដឹង — និមិត្តសញ្ញាបែបបុរាណមួយ\n"
        "⭐ ផ្កាយ — និមិត្តសញ្ញាដែលប្រើក្នុងប្រធានបទផ្សេងៗ\n"
        "7️⃣ លេខប្រាំពីរ — ប្រើជាញឹកញាប់ក្នុងហ្គេមបែបបុរាណ\n"
        "🃏 Wild — អាចជំនួសនិមិត្តសញ្ញាផ្សេងៗបាន អាស្រ័យលើច្បាប់ហ្គេម\n"
        "❓ Scatter — អាចបើកមុខងារពិសេសក្នុងហ្គេមខ្លះៗ\n\n"
        "ត្រូវពិនិត្យច្បាប់របស់ហ្គេមនីមួយៗជានិច្ច ព្រោះនិមិត្តសញ្ញាមិនមានតម្លៃដូចគ្នាគ្រប់ហ្គេមទេ។"
    ),
    "reels": (
        "🎰 ស្គ្រីនវិល និងបន្ទាត់\n\n"
        "ស្គ្រីនវិល គឺជាជួរឈរដែលបង្ហាញនិមិត្តសញ្ញា។ ហ្គេមអាចមាន ៣, ៥ ឬចំនួនផ្សេងទៀត។\n\n"
        "• បន្ទាត់ឈ្នះ (Payline)៖ លំនាំដែលហ្គេមប្រើដើម្បីពិនិត្យការផ្គូផ្គងនិមិត្តសញ្ញា\n"
        "• វិធីឈ្នះ (Ways-to-win)៖ វិធីរាប់និមិត្តសញ្ញាដែលត្រូវគ្នាតាមស្គ្រីនវិលជាប់គ្នា\n"
        "• ក្រឡា (Grid)៖ ការរៀបចំនិមិត្តសញ្ញាទាំងអស់ដែលមើលឃើញ\n\n"
        "ហ្គេមនីមួយៗមានច្បាប់ផ្ទាល់ខ្លួន។ លទ្ធផលមុនៗមិនអាចទាយលទ្ធផលបន្ទាប់បានទេ។"
    ),
    "bonus": (
        "✨ មុខងារបន្ថែម\n\n"
        "ហ្គេមខ្លះអាចមានមុខងារបន្ថែម ដូចជា៖\n\n"
        "• ជុំបង្វិលឥតគិតថ្លៃ (Free Spins)\n"
        "• និមិត្តសញ្ញា Wild ដែលមានរបៀបដំណើរការពិសេស\n"
        "• មុខងារដែលបើកដោយនិមិត្តសញ្ញា Scatter\n"
        "• មេគុណ ឬនិមិត្តសញ្ញាដែលពង្រីកទំហំ\n\n"
        "មុខងារ និងច្បាប់អាស្រ័យលើហ្គេមនីមួយៗ។ មុខងារបន្ថែមមិនធានាលទ្ធផលណាមួយឡើយ។"
    ),
    "paylines": (
        "📐 ការយល់ដឹងអំពីបន្ទាត់ឈ្នះ\n\n"
        "បន្ទាត់ឈ្នះ (Payline) គឺជាផ្លូវដែលបានកំណត់ទុក ដើម្បីឱ្យហ្គេមពិនិត្យការផ្គូផ្គងនិមិត្តសញ្ញានៅលើស្គ្រីនវិល។ "
        "ហ្គេមខ្លះមានបន្ទាត់ថេរ ហ្គេមខ្លះអាចជ្រើសរើសបន្ទាត់បាន ហើយហ្គេមផ្សេងទៀតប្រើប្រព័ន្ធ Ways-to-win ឬការផ្គូផ្គងជាក្រុមក្រឡា។ "
        "សូមអានព័ត៌មានរបស់ហ្គេម ដើម្បីដឹងថាវាប្រើប្រព័ន្ធណា។"
    ),
    "rng": (
        "🎲 ភាពចៃដន្យ និងការរំពឹងទុកត្រឹមត្រូវ\n\n"
        "ហ្គេមស្លូតឌីជីថលជាច្រើនប្រើម៉ាស៊ីនបង្កើតលេខចៃដន្យ (RNG) ដើម្បីកំណត់លទ្ធផល។ "
        "ក្នុងហ្គេម RNG ដែលរចនាបានត្រឹមត្រូវ ការបង្វិលនីមួយៗឯករាជ្យពីគ្នា៖ លទ្ធផលមុនមិនមានន័យថាលទ្ធផលឈ្នះត្រូវតែកើតឡើងបន្ទាប់ ឬអាចទាយលទ្ធផលបន្ទាប់បានទេ។ "
        "បូតនេះមិនអាចទាយលទ្ធផល ឬធានាការឈ្នះបានឡើយ។"
    ),
    "help": (
        "ℹ️ របៀបប្រើបូតនេះ\n\n"
        "ចុចប៊ូតុងក្នុងម៉ឺនុយ ដើម្បីអានប្រធានបទដែលអ្នកចាប់អារម្មណ៍។ អ្នកក៏អាចប្រើពាក្យបញ្ជាខាងក្រោម៖\n"
        "/start — បើកម៉ឺនុយមេ\n"
        "/info — ព័ត៌មានអំពីបូតនេះ\n"
        "/symbols — មគ្គុទ្ទេសក៍អំពីនិមិត្តសញ្ញា\n"
        "/reels — ព័ត៌មានអំពីស្គ្រីនវិល និងបន្ទាត់\n"
        "/help — បង្ហាញជំនួយ\n\n"
        "សម្រាប់ព័ត៌មាន និងចំណេះដឹងប៉ុណ្ណោះ។ មិនមានការភ្នាល់ ការលេងដោយប្រើប្រាក់ពិត រង្វាន់ ឬការដកប្រាក់ទេ។"
    ),
}

MENU_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🎨 និមិត្តសញ្ញា", callback_data="symbols"),
        InlineKeyboardButton("ស្គ្រីនវិល និងរបៀបដំណើរការ", callback_data="reels"),
    ],
    [
        InlineKeyboardButton("✨ មុខងារបន្ថែម", callback_data="bonus"),
        InlineKeyboardButton("📐 បន្ទាត់ឈ្នះ", callback_data="paylines"),
    ],
    [
        InlineKeyboardButton("🎲 ភាពចៃដន្យ", callback_data="rng"),
        InlineKeyboardButton("ℹ️ អំពីបូត", callback_data="info"),
    ],
    [InlineKeyboardButton("❔ ជំនួយ", callback_data="help")],
])

BACK_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🏠 ម៉ឺនុយមេ", callback_data="menu")],
    [
        InlineKeyboardButton("⬅️ និមិត្តសញ្ញា", callback_data="symbols"),
        InlineKeyboardButton("➡️ ស្គ្រីនវិល", callback_data="reels"),
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
        await query.answer("មិនស្គាល់ជម្រើសនេះទេ។", show_alert=True)
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
    await application.bot.set_my_name(BOT_NAME)
    await application.bot.set_my_commands([
        BotCommand("start", "បើកម៉ឺនុយមេ"),
        BotCommand("info", "ព័ត៌មានអំពីបូតនេះ"),
        BotCommand("symbols", "អានអំពីនិមិត្តសញ្ញា"),
        BotCommand("reels", "អានអំពីស្គ្រីនវិល និងបន្ទាត់"),
        BotCommand("help", "បង្ហាញជំនួយ"),
    ])
    await application.bot.set_my_description(
        "ព័ត៌មានទូទៅជាភាសាខ្មែរ អំពីហ្គេមស្លត រួមមាននិមិត្តសញ្ញា ស្គ្រីនវិល ច្បាប់ និងមុខងាររបស់ហ្គេម។ សម្រាប់ការអប់រំ និងចំណេះដឹងប៉ុណ្ណោះ។"
    )
    await application.bot.set_my_short_description(
        "ព័ត៌មានទូទៅ និងចំណេះដឹងអំពីហ្គេមស្លត ជាភាសាខ្មែរ។"
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
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Starting %s", BOT_NAME)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
