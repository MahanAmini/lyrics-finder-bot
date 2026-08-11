import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN: str | None=os.getenv("TELEGRAM_BOT_TOKEN")
GENIUS_API_KEY:str | None=os.getenv("GENIUS_API_KEY")

def validate_config() -> None:
    missing: list[str] = []

    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not GENIUS_API_KEY:
        missing.append("GENIUS_API_KEY")

    if missing:
        logger.error("Environmental variables in .env has not set correctly : %s",
            ", ".join(missing),)
        sys.exit(1)

    logger.info("Settings has been loading successfully.")