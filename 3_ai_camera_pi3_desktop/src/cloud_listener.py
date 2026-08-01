import time
import threading
from supabase import create_client, Client
from src.config import Config

class CloudListener:
    def __init__(self, event_queue):
        # Orthogonality: The listener knows nothing of the UI or Camera.
        # It only interacts with Supabase and puts abstract events onto a thread-safe Queue.
        self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        self.event_queue = event_queue
        self.last_seen_id = None
        self._running = False

    def _get_latest_transaction(self):
        # CLRS: Database retrieval bounded to \mathcal{O}(1) time by leveraging LIMIT 1.
        response = self.supabase.table("transactions_log").select("*").order("created_at", desc=True).limit(1).execute()
        return response.data[0] if response.data else None

    def _poll(self):
        while self._running:
            try:
                latest = self._get_latest_transaction()
                if latest and latest.get("id") != self.last_seen_id:
                    if self.last_seen_id is not None:
                        # New transaction detected, fire event
                        self.event_queue.put(latest)
                    self.last_seen_id = latest.get("id")
            except Exception as e:
                print(f"[Supabase Polling Error]: {e}")
            
            time.sleep(2) # Polling interval

    def start(self):
        self._running = True
        thread = threading.Thread(target=self._poll, daemon=True)
        thread.start()