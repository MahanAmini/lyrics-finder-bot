import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.language_service import get_message
import httpx
import re

logger = logging.getLogger(__name__)

async def get_track_info_scrape(track_id: str):
    url = f"https://open.spotify.com/track/{track_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    html = response.text

    title_match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    song_name = title_match.group(1) if title_match else None

    desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    description = desc_match.group(1) if desc_match else None

    artist_name = None
    if description:
        parts = description.split(" · ")
        if len(parts) > 0:
            artist_name = parts[0]

    return [song_name, artist_name]

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

    track_payload = context.args[0] if context.args else None
    if track_payload:
        track_id = track_payload.split('_')[0]
        logger.info("User: %s requested track_id: %s", user.id, track_id)
        track = await get_track_info_scrape(track_id)
        song_name, artist_name = track
        context.args = song_name.split() + ["by"] + artist_name.split()
        from handlers.search import accurate_search_handler
        await accurate_search_handler(update, context)
        return

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
