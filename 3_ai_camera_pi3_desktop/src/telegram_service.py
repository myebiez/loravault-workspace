import requests
from src.config import Config

class TelegramNotifier:
    def __init__(self):
        # Pragmatic: Design by Contract. Fail fast if configuration is missing.
        assert Config.TELEGRAM_BOT_TOKEN, "Telegram Bot Token is missing"
        assert Config.TELEGRAM_CHAT_ID, "Telegram Chat ID is missing"
        self.base_url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}"

    def send_audit(self, message, image_path):
        # Decoupled notification emitter.
        url = f"{self.base_url}/sendPhoto"
        try:
            with open(image_path, 'rb') as photo:
                payload = {"chat_id": Config.TELEGRAM_CHAT_ID, "caption": message}
                files = {"photo": photo}
                response = requests.post(url, data=payload, files=files, timeout=10)
                response.raise_for_status()
        except Exception as e:
            print(f"[Network Error] Telegram dispatch failed: {e}")