import logging
import config
from telegram import BotCommand
from telegram.ext import Application, CommandHandler,MessageHandler, filters,CallbackQueryHandler
from handlers.start import start_command
from handlers.search import search_handler,button_click_handler,accurate_search_handler,start_button_handler
from handlers.language import language_handler,button_language_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def setup_bot_commands(application):
    commands = [
        BotCommand("start", "Let's Start - Home Page"),
        BotCommand("search", "Manual Search"),
        BotCommand("language", "Change Bot language"),
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    config.validate_config()

    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).concurrent_updates(True).post_init(setup_bot_commands).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("search", accurate_search_handler))
    application.add_handler(CommandHandler("language", language_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))
    application.add_handler(CallbackQueryHandler(button_click_handler,pattern=r"^\d+$"))
    application.add_handler(CallbackQueryHandler(start_button_handler, pattern=r"^(about|guide|home$)$"))
    application.add_handler(CallbackQueryHandler(button_language_handler, pattern=r"^lang_(fa|en)$"))

    logger.info("Bot is running | (polling mode) ...")

    application.run_polling()

if __name__ == "__main__":
    main()