from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from handlers.start import start_command
from services.lyrics_service import search_songs_itunes, get_lyrics_with_fallback, get_artwork_url
from utils import split_text
from services.language_service import get_message

logger = logging.getLogger(__name__)

"""
async def search_handler_genius(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user = update.effective_user
    user_id = user.id if user else "Unknown"
    logger.info("Message: %s from this User: %s is received now.", message, user_id)
    lyrics: str | None = await get_lyrics_genius(message)
    if lyrics is None:
        logger.info('Music: %s requested from User: %s is not found!', message, user_id)
        await update.message.reply_text(f'Music: {message} is not found!')
    else:
        logger.info('Music: %s requested from User: %s is found successfully.', message, user_id)
        await update.message.reply_text(lyrics)


async def search_handler_ovh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    message = message.split('-')
    user = update.effective_user
    user_id = user.id if user else "Unknown"
    logger.info("Message: %s from this User: %s is received now.", message, user_id)
    lyrics: str | None = await get_lyrics_ovh(message[0], message[1])
    if lyrics is None:
        logger.info('Music: %s requested from User: %s is not found!', message, user_id)
        await update.message.reply_text(f'Music: {message} is not found!')
    else:
        logger.info('Music: %s requested from User: %s is found successfully.', message[0], user_id)
        await update.message.reply_text(lyrics)


async def search_handler_lrclib(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    message = message.split('-')
    user = update.effective_user
    user_id = user.id if user else "Unknown"
    logger.info("Message: %s from this User: %s is received now.", message, user_id)
    lyrics: str | None = await get_lyrics_lrclib(message[0], message[1])
    if lyrics is None:
        logger.info('Music: %s requested from User: %s is not found!', message, user_id)
        await update.message.reply_text(f'Music: {message} is not found!')
    else:
        logger.info('Music: %s requested from User: %s is found successfully.', message[0], user_id)
        await update.message.reply_text(lyrics)


"""


async def start_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    user_id = str(user.id)
    if query.data == "home":
        await start_command(update, context)
        return

    response = get_message(query.data, user_id)
    keyboard = [
        [InlineKeyboardButton("🏠 Home", callback_data="home")],
    ]
    keyboard_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_caption(response, parse_mode=ParseMode.HTML, reply_markup=keyboard_markup)


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user = update.effective_user
    user_id = user.id if user else "Unknown"
    logger.info("Message: %s from this User: %s is received now.", message, user_id)
    songs: list[dict[str, str]] | None = await search_songs_itunes(message)
    if not songs:
        logger.info("Nothing found for: %s", message)
        response = get_message("music_not_found", str(user_id), message=message)
        await update.message.reply_text(response)
        return

    context.user_data["search_results"] = songs
    keyboard = []
    for index, item in enumerate(songs):
        button_text = f"{item['trackName']} by {item['artistName']}"
        button = InlineKeyboardButton(button_text, callback_data=str(index))
        keyboard.append([button])
    markup = InlineKeyboardMarkup(keyboard)
    response = get_message("choose_song", str(user_id))
    await update.message.reply_text(response, reply_markup=markup)


async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    index = int(query.data)
    user = update.effective_user
    user_id = str(user.id)
    artist_name = context.user_data["search_results"][index]["artistName"]
    song_name = context.user_data["search_results"][index]["trackName"]
    song_cover = context.user_data["search_results"][index]["artworkUrl100"]

    response = get_message("searching_song", user_id, song_name=song_name, artist_name=artist_name)
    gif_file_id = "CgACAgQAAxkBAAIBWGp3wBeaxLLzC_vV7AiF8-rrYsiLAALbAgACaXQNU5iTd6iTXJl7PQQ"
    await query.message.reply_animation(animation=gif_file_id,
                                        caption=response,
                                        reply_to_message_id=query.message.message_id)

    lyrics = await get_lyrics_with_fallback(song_name, artist_name)
    if lyrics is None:
        response = get_message("song_not_found_all", user_id, message=song_name, song_name=song_name,
                               artist_name=artist_name)
        gif_file_id = "CgACAgUAAxkBAAIBWmp3w0mW1uUJe82P0JTAhSgAAZtqEQACUwQAArQFQVQnLvyJJKANMD0E"
        await query.message.reply_animation(animation=gif_file_id,
                                            caption=response,
                                            reply_to_message_id=query.message.message_id)
    else:
        logger.info("Music: %s by %s found successfully.", song_name, artist_name)
        response = get_message("song_info", user_id, song_name=song_name, artist_name=artist_name)
        await query.message.reply_photo(photo=song_cover, caption=response)
        chunks = split_text(lyrics)
        for chunk in chunks:
            await query.message.reply_text(chunk)


async def accurate_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id if user else "Unknown"

    full_text = " ".join(context.args)
    parts = full_text.split(" by ")

    gif_file_id = "CgACAgQAAxkBAAIBRGp3u_XTmBF_ix3PziC90dmQOFonAAI_BQACeSYMUtm0ZtXA9w-5PQQ"

    if len(parts) != 2:
        logger.info("Invalid /search format from user %s: '%s'", user_id, full_text)
        response = get_message("invalid_format", str(user_id))
        await update.message.reply_animation(animation=gif_file_id, caption=response,
                                             reply_to_message_id=update.message.message_id)
        return

    song_name = parts[0].strip()
    artist_name = parts[1].strip()

    logger.info("Accurate search: '%s' by '%s' from user %s", song_name, artist_name, user_id)
    response = get_message("searching_song", user_id, song_name=song_name, artist_name=artist_name)
    gif_file_id = "CgACAgQAAxkBAAIBWGp3wBeaxLLzC_vV7AiF8-rrYsiLAALbAgACaXQNU5iTd6iTXJl7PQQ"
    await update.message.reply_animation(animation=gif_file_id,
                                         caption=response,
                                         reply_to_message_id=update.message.message_id)

    lyrics = await get_lyrics_with_fallback(song_name, artist_name)
    song_cover = await get_artwork_url(song_name, artist_name)

    if lyrics is None:
        logger.info("Music: %s by %s is not found at all!", song_name, artist_name)
        gif_file_id = "CgACAgUAAxkBAAIBWmp3w0mW1uUJe82P0JTAhSgAAZtqEQACUwQAArQFQVQnLvyJJKANMD0E"
        response = get_message("song_not_found_all", user_id, message=song_name, song_name=song_name,
                               artist_name=artist_name)
        await update.message.reply_animation(animation=gif_file_id,
                                             caption=response,
                                             reply_to_message_id=update.message.message_id)
    else:
        logger.info("Music: %s by %s found successfully.", song_name, artist_name)
        if song_cover:
            response = get_message("song_info", user_id, song_name=song_name, artist_name=artist_name)
            await update.message.reply_photo(photo=song_cover, caption=response)
        chunks = split_text(lyrics)
        for chunk in chunks:
            await update.message.reply_text(chunk)
