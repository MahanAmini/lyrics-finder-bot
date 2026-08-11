import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.language_service import get_message

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = str(user.id)
    welcome_text = get_message("welcome", user_id, name=user.first_name)
    about_btn = get_message("about_btn", user_id)
    developer_btn = get_message("developer_btn", user_id)
    guide_btn = get_message("guide_btn", user_id)
    keyboard = [
        [InlineKeyboardButton(about_btn, callback_data="about"),
         InlineKeyboardButton(developer_btn, url="https://t.me/Mahan_aminy"),
         InlineKeyboardButton(guide_btn, callback_data="guide")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_caption(caption=welcome_text, reply_markup=markup)
        logger.info("User: %s runs command /start -> button home", user.id if user else "Unknown")
        return

    if update.message:
        logger.info("User: %s runs command /start", user.id if user else "Unknown")
        bot_id = context.bot.id
        photos = await context.bot.get_user_profile_photos(user_id=bot_id)
        file_id = None
        if photos.total_count > 0:
            file_id = photos.photos[0][-1].file_id
        await update.message.reply_photo(photo=file_id, caption=welcome_text, reply_markup=markup,
                                         reply_to_message_id=update.message.message_id)
