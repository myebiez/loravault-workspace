import os
from dotenv import load_dotenv

load_dotenv()

# SICP: Data Abstraction. Centralizing external dependencies.
class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # Krug: Visual definitions stored as constants to enforce consistent DOET signifiers.
    COLOR_BG = "#18181b"
    COLOR_SUCCESS = "#16a34a" # Clear Green
    COLOR_ALERT = "#dc2626"   # High-Contrast Red
    COLOR_TEXT = "#ffffff"