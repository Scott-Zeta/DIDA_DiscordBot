import os
from dotenv import load_dotenv

load_dotenv()

# Discord bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")