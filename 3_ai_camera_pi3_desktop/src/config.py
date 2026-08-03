import os
from dotenv import load_dotenv

load_dotenv()

# SICP: Data Abstraction. Centralizing external dependencies.
class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    GATEWAY_TOKEN = os.getenv("GATEWAY_TOKEN") # Injeksi Token Kriptografis
    
    # UI/UX: Executive Premium Theme (Palantir/Bloomberg terminal aesthetic)
    # Krug's Rule 8 (Visual Hierarchy) & Norman's Signifiers: High contrast, semantic colors.
    COLOR_BG = "#0f172a"          # Slate 900 (Deep, elegant dark background)
    COLOR_SUCCESS = "#10b981"     # Emerald 500 (Calm, definitive secure state)
    COLOR_ALERT = "#e11d48"       # Rose 600 (Urgent, unmissable action state)
    COLOR_TEXT_MAIN = "#f8fafc"   # Slate 50 (Crisp readability)
    COLOR_TEXT_MUTED = "#94a3b8"  # Slate 400 (For secondary information)