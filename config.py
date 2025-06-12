import os
from dotenv import load_dotenv
from utils.logger import Logger

load_dotenv()
log = Logger("config")

# Discord bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    log.critical("Missing environment variable: BOT_TOKEN")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    log.warning("GEMINI_API_KEY is not set — Gemini features may not work.")