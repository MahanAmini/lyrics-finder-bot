from telegram.ext import ContextTypes
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from services.language_service import set_user_language,get_message

logger = logging.getLogger(__name__)

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_en"),InlineKeyboardButton("Persian",callback_data="lang_fa")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    logger.info("%s Wants to change language", user.id)
    response = get_message("ask_language",str(user.id))
    await update.message.reply_text(response, reply_markup=markup)


content = {
    "lang_en" : "English",
    "lang_fa" : "Persian",
}
async def button_language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    query_data = query.data
    user = update.effective_user
    user_id = user.id if user else "Unknown"
    language_code = query_data.replace("lang_", "")
    set_user_language(user_id, language_code)
    logger.info("%s changes the language to %s", user_id,content[query_data])
    response = get_message("language_selected",str(user_id),name=user.first_name,language=content[query_data])
    await query.edit_message_text(response)