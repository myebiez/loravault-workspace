import requests
from src.config import Config

class TelegramNotifier:
    def __init__(self):
        # Pragmatic: Design by Contract. Fail fast if configuration is missing.
        assert Config.TELEGRAM_BOT_TOKEN, "Telegram Bot Token is missing"
        assert Config.TELEGRAM_CHAT_ID, "Telegram Chat ID is missing"
        self.base_url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}"

    def send_audit(self, message: str, image_path: str):
        """
        Decoupled notification emitter.
        Mengirim foto lokal sebagai preview cepat, beserta caption yang 
        kini berisi tautan permanen (SSOT) ke Supabase Storage.
        """
        url = f"{self.base_url}/sendPhoto"
        try:
            with open(image_path, 'rb') as photo:
                # parse_mode 'Markdown' enables bolding and hyperlink rendering
                payload = {
                    "chat_id": Config.TELEGRAM_CHAT_ID, 
                    "caption": message, 
                    "parse_mode": "Markdown"
                }
                files = {"photo": photo}
                
                # Jaringan bisa berfluktuasi, set timeout yang rasional
                response = requests.post(url, data=payload, files=files, timeout=15)
                
                # Feedback Logging (DOET: Visibilitas Sistem)
                if response.status_code == 200:
                    print("[Telegram Success] Push notification sent to Executive channel.")
                else:
                    print(f"[Telegram Warning] Failed to send message. HTTP {response.status_code}: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            # Kegagalan notifikasi Telegram TIDAK BOLEH membuat sistem crash.
            # Bukti utama sudah aman di Supabase Storage (SSOT).
            print(f"[Network Error] Telegram dispatch failed: {e}")
        except Exception as e:
            print(f"[System Error] Telegram service encountered an unexpected error: {e}")