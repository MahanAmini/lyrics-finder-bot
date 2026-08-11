import asyncio
from urllib.parse import quote
from lyricsgenius import Genius
import logging

from telegram import Update

import config
import requests

genius = Genius(config.GENIUS_API_KEY)

logger = logging.getLogger(__name__)


async def get_lyrics_genius(song_name: str, artist_name: str | None = None) -> str | None:
    logger.info("Searching for Music : %s (Artist: %s)",
                song_name,
                artist_name or "Unknown", )
    try:
        song = await asyncio.to_thread(genius.search_song, song_name, artist_name)
    except Exception as e:
        logger.warning("Genius request failed for '%s': %s", song_name, e)
        return None

    if song is None:
        logger.warning("Music: %s is not found!", song_name)
        return None

    logger.info("Music: %s has founded successfully at genius", song_name)
    return song.lyrics


async def get_lyrics_ovh(song_name: str, artist_name: str | None = None) -> str | None:
    urlFormat = f'https://api.lyrics.ovh/v1/{quote(artist_name)}/{quote(song_name)}'
    try:
        response = await asyncio.to_thread(requests.get, urlFormat)
    except Exception as e:
        logger.warning("OVH request failed for '%s': %s", song_name, e)
        return None

    song = response.json()

    if response.status_code != 200:
        logger.warning("Music: %s is not found!", song_name)
        return None
    else:
        logger.info("Music: %s has founded successfully at ovh", song_name)
        return song["lyrics"]


async def get_lyrics_lrclib(song_name: str, artist_name: str | None = None) -> str | None:
    urlFormat = "https://lrclib.net/api/get"
    params = {"track_name": song_name, "artist_name": artist_name}
    try:
        response = await asyncio.to_thread(requests.get, urlFormat, params=params)
    except Exception as e:
        logger.warning("Lrclib request failed for '%s': %s", song_name, e)
        return None

    song = response.json()
    if response.status_code != 200:
        logger.warning("Music: %s is not found!", song_name)
        return None
    else:
        logger.info("Music: %s has founded successfully at lrclib", song_name)
        return song['plainLyrics']


async def search_songs_itunes(song_name: str) -> list[dict[str, str]]:
    url_format = "https://itunes.apple.com/search"
    params = {"term": song_name, "entity": "song", "limit": 10}
    response = await asyncio.to_thread(requests.get, url_format, params=params)

    if response.status_code == 200:
        data = response.json()
        songs = [
            {"artistName": item["artistName"], "trackName": item["trackName"],
             "artworkUrl100": item["artworkUrl100"].replace("100x100", "600x600")}
            for item in data["results"]
        ]
        logger.info("%s results with %s founded.", data["resultCount"], song_name)
        return songs
    return []


async def get_artwork_url(song_name: str, artist_name: str) -> str | None:
    query = f"{song_name} {artist_name}"
    results = await search_songs_itunes(query)

    if not results:
        logger.info("No artwork found for '%s' by '%s'.", song_name, artist_name)
        return None

    artwork_url = results[0].get("artworkUrl100")

    if not artwork_url:
        logger.info("First result has no artwork for '%s'.", song_name)
        return None

    return artwork_url.replace("100x100", "600x600")


async def get_lyrics_with_fallback(song_name: str, artist_name: str | None = None) -> str | None:
    lyrics: str | None = await get_lyrics_genius(song_name, artist_name)
    if lyrics is None:
        logger.info("Music: %s is not found at genius.", song_name)
        lyrics = await get_lyrics_lrclib(song_name, artist_name)

    if lyrics is None:
        logger.info("Music: %s is not found at lrclib.", song_name)
        lyrics = await get_lyrics_ovh(song_name, artist_name)

    if lyrics is None:
        logger.info("Music: %s is not found at all!", song_name)
        return None

    logger.info("Music: %s is found successfully.", song_name)
    return lyrics


"""
async def main():
    result = await search_songs_itunes("gole man")
    print(result)

asyncio.run(main())
"""
